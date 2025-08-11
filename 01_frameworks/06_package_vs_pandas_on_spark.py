#!/usr/bin/env python3
"""
Frameworks: External package (Numba/NumPy) vs pandas-on-Spark for model scoring
================================================================================

Experiment: score a model that requires complex feature transforms and
multi-step iterative forecasts per entity over dozens of periods.

Compare two approaches:
1) External package implemented with NumPy/Numba (see utils/modelpkg.py),
   run on single machine after Spark→pandas (Arrow); treat Spark as ETL.
2) pandas-on-Spark (ps) implementation to keep work inside Spark executor
   plan while using pandas-like API.

Outcome guidance:
- Small to medium data, heavy numeric kernels, iterative loops: package+Numba
  wins after Arrow conversion. Best when data fits in driver memory and
  kernels are compute-bound.
- Larger-than-memory or cluster-scaling need, group/window-heavy ops without
  tight per-row loops: pandas-on-Spark (or native Spark) is better. Avoid
  Python crossings and shipping big data to driver.
"""

from __future__ import annotations

import os
import sys
import time
import numpy as np

# Ensure utils importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.mem import get_total_memory_gb
from utils.modelpkg import transform_features, iterative_forecast, has_numba

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col


def _fix_numpy_compatibility() -> None:
    os.environ.setdefault("PYARROW_IGNORE_TIMEZONE", "1")
    if not hasattr(np, "NaN") and hasattr(np, "nan"):
        np.NaN = np.nan  # type: ignore[attr-defined]


def build_spark_data(spark: SparkSession, rows: int, entities: int, wide_cols: int = 0):
    from pyspark.sql.window import Window

    # Create panel: entity_id × t with synthetic inputs
    base = spark.range(rows).select(
        (col("id") % entities).alias("entity_id"),
        col("id").alias("t"),
        (F.rand() * 100.0).alias("values"),
        (F.rand() * 50.0 + 10.0).alias("prices"),
        (F.rand() > 0.5).cast("int").alias("flag"),
        (F.rand() * 5).cast("int").alias("cat"),
    )

    # Add wide columns to simulate hundreds of features (not used by model here
    # but they materially impact conversion and ps dataframe width)
    if wide_cols > 0:
        for i in range(wide_cols):
            base = base.withColumn(f"w_{i}", F.rand())

    # Optional: ensure per-entity ordering
    w = Window.partitionBy("entity_id").orderBy(col("t").asc())
    df = base.select("entity_id", "t", "values", "prices", "flag", "cat", *[f"w_{i}" for i in range(wide_cols)])
    return df.cache()


def run_package_path(spark: SparkSession, df, horizon: int):
    def to_pandas():
        # Only convert columns used by the model to reduce width
        slim = df.select("entity_id", "values", "prices", "flag", "cat")
        return slim.toPandas()

    print("\n== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==")
    t0 = time.time()
    try:
        pdf = to_pandas()
    except Exception as e:
        print(f"   ⚠️ Spark→pandas conversion failed (skipping package path): {str(e)[:120]}...")
        return None
    t_conv = time.time() - t0

    # Prepare arrays
    entity = pdf["entity_id"].values.astype(np.int64)
    values = pdf["values"].values.astype(np.float64)
    prices = pdf["prices"].values.astype(np.float64)
    exog = np.stack([
        pdf["flag"].values.astype(np.float64),
        pdf["cat"].values.astype(np.float64),
    ], axis=1)

    # Feature transform
    t1 = time.time()
    base = transform_features(values, prices, exog)
    t_tf = time.time() - t1

    # Iterative forecast per entity
    t2 = time.time()
    y = iterative_forecast(entity, base, horizon=horizon, alpha=0.3, beta=0.6)
    t_fc = time.time() - t2

    print(f"   Convert (Arrow): {t_conv:.3f}s; transform: {t_tf:.3f}s; forecast: {t_fc:.3f}s")
    return {"convert": t_conv, "transform": t_tf, "forecast": t_fc, "numba": has_numba()}


def run_pandas_on_spark(spark: SparkSession, df, horizon: int):
    print("\n== Spark path (pandas-like logic via Spark SQL functions) ==")
    _fix_numpy_compatibility()

    # Keep only required columns to limit width
    sdf = df.select("entity_id", "t", "values", "prices", "flag", "cat")

    # Vectorizable transform using Spark expressions (no NumPy)
    t0 = time.time()
    sdf = sdf.withColumn(
        "feat",
        0.15 * (col("values") * col("prices"))
        + 0.07 * (col("values") ** F.lit(0.5))
        + 0.03 * (col("prices") ** F.lit(1.5))
        + 0.10 * (col("flag").cast("double") * col("values"))
        + 0.02 * (col("cat").cast("double") * col("prices")),
    )
    _ = sdf.select(F.avg("feat")).collect()  # materialize
    t_tf = time.time() - t0

    # Iterative forecast via repeated column updates (still runs in Spark)
    t1 = time.time()
    sdf = sdf.withColumn("y", F.lit(0.0))
    for _ in range(horizon):
        sdf = sdf.withColumn("y", 1.0 / (1.0 + F.exp(-(0.3 * col("feat") + 0.6 * col("y")))))
    _ = sdf.select(F.avg("y")).collect()  # materialize
    t_fc = time.time() - t1

    print(f"   transform(spark): {t_tf:.3f}s; forecast(spark, {horizon} steps): {t_fc:.3f}s")
    return {"transform": t_tf, "forecast": t_fc}


def _estimate_bytes(rows: int, cols: int, dtype_bytes: int = 8) -> float:
    return float(rows) * float(cols) * float(dtype_bytes)


def run_scenario(spark: SparkSession, name: str, rows: int, entities: int, horizon: int, wide_cols: int, mem_gb: float):
    print("\n" + "=" * 80)
    print(f"🧪 Scenario: {name}")
    print("-" * 80)
    print(f"rows={rows:,}, entities={entities:,}, horizon={horizon}, wide_cols={wide_cols}")
    cols_for_est = 6 + wide_cols  # entity_id,t,values,prices,flag,cat + wide
    est_bytes = _estimate_bytes(rows, cols_for_est, 8)
    print(f"~Estimated raw size (double-eqv): {est_bytes/1e9:.2f} GB")

    df = build_spark_data(spark, rows=rows, entities=entities, wide_cols=wide_cols)
    cnt = df.count(); print(f"   Built panel rows: {cnt:,}")

    # Run package path only if reasonably safe
    pkg = None
    safety_factor = 0.5  # allow up to 50% of RAM for DataFrame conversion
    if (est_bytes / (1024**3)) < mem_gb * safety_factor:
        pkg = run_package_path(spark, df, horizon=horizon)
    else:
        print("   ⚠️ Skipping package path: dataset too large to safely collect to driver")

    ps = run_pandas_on_spark(spark, df, horizon=horizon)

    # Summary
    print("\n📊 Scenario summary:")
    if pkg:
        total_pkg = pkg["convert"] + pkg["transform"] + pkg["forecast"]
        print(f"   Package path total: {total_pkg:.3f}s  (convert={pkg['convert']:.3f}s, tf={pkg['transform']:.3f}s, fc={pkg['forecast']:.3f}s, numba={pkg['numba']})")
    else:
        print("   Package path total: n/a (skipped)")
    if ps:
        total_ps = ps["transform"] + ps["forecast"]
        print(f"   pandas-on-Spark total: {total_ps:.3f}s (tf={ps['transform']:.3f}s, fc={ps['forecast']:.3f}s)")
    else:
        print("   pandas-on-Spark total: n/a (ps unavailable)")

    print("\n🧭 Guidance:")
    print("   • Package path excels when compute is heavy (large horizon) and data fits in memory.")
    print("   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.")


def main():
    print("🚀 Package vs pandas-on-Spark experiment")
    print("📚 Docs index: docs/index.md")
    mem = get_total_memory_gb()
    print(f"💻 System memory: {mem:.1f} GB")

    spark = (
        SparkSession.builder.appName("Package-vs-PandasOnSpark")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.sql.execution.arrow.maxRecordsPerBatch", "2000")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Scenarios matrix (demonstrates pros/cons)
    scenarios = [
        ("Small, in-memory compute-heavy (Numba sweet spot)", 300_000, 500, 48, 0),
        ("Medium, some width (balanced)", 600_000, 1_000, 36, 50),
        ("Wide (hundreds cols), moderate horizon", 400_000, 1_000, 24, 200),
        ("Large rows (driver-safety block), horizon small", 2_000_000, 2_000, 12, 50),
    ]

    for name, rows, entities, horizon, wide_cols in scenarios:
        run_scenario(spark, name, rows, entities, horizon, wide_cols, mem)

    spark.stop()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/06_package_vs_pandas_on_spark.md",
            title="Frameworks: Package (Numba/NumPy) vs pandas-on-Spark",
            main_callable=main,
        )
    else:
        main()



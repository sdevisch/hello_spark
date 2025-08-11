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


def build_spark_data(spark: SparkSession, rows: int, entities: int):
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

    # Optional: ensure per-entity ordering
    w = Window.partitionBy("entity_id").orderBy(col("t").asc())
    df = base.select("entity_id", "t", "values", "prices", "flag", "cat")
    return df.cache()


def run_package_path(spark: SparkSession, df, horizon: int):
    def to_pandas():
        return df.toPandas()

    print("\n== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==")
    t0 = time.time()
    pdf = to_pandas()
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
    print("\n== pandas-on-Spark path: keep work in Spark plan ==")
    try:
        import pyspark.pandas as ps
    except Exception as e:
        print(f"   pandas-on-Spark unavailable: {e}")
        return None

    # Create ps.DataFrame from Spark df
    psdf = ps.DataFrame(df)

    # Vectorizable part as column expressions (avoid tight Python loops)
    t0 = time.time()
    psdf = psdf.assign(
        feat=0.15 * (psdf.values * psdf.prices)
             + 0.07 * (psdf.values ** 0.5)
             + 0.03 * (psdf.prices ** 1.5)
             + 0.10 * (psdf.flag * psdf.values)
             + 0.02 * (psdf.cat * psdf.prices)
    )
    t_tf = time.time() - t0

    # Iterative forecast across horizon is not friendly to ps; emulate with
    # repeated map (still executes as Spark jobs). This highlights where 
    # pandas-on-Spark is less suited than a compiled kernel.
    t1 = time.time()
    y = psdf.feat
    for _ in range(horizon):
        y = 1.0 / (1.0 + np.exp(-(0.3 * psdf.feat + 0.6 * y)))
    # Force materialization (e.g., count)
    _ = y.to_frame().count()
    t_fc = time.time() - t1

    print(f"   transform(ps): {t_tf:.3f}s; forecast(ps, {horizon} steps): {t_fc:.3f}s")
    return {"transform": t_tf, "forecast": t_fc}


def main():
    print("🚀 Package vs pandas-on-Spark experiment")
    print("📚 Docs index: docs/index.md")
    mem = get_total_memory_gb()
    print(f"💻 System memory: {mem:.1f} GB")

    # Size knobs
    if mem < 8:
        rows, entities, horizon = 300_000, 500, 24
    elif mem < 16:
        rows, entities, horizon = 600_000, 1_000, 36
    else:
        rows, entities, horizon = 1_000_000, 2_000, 48

    spark = (
        SparkSession.builder.appName("Package-vs-PandasOnSpark")
        .master("local[*]")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Build data
    df = build_spark_data(spark, rows=rows, entities=entities)
    cnt = df.count(); print(f"   Built panel rows: {cnt:,}")

    # Run paths
    pkg = run_package_path(spark, df, horizon=horizon)
    ps = run_pandas_on_spark(spark, df, horizon=horizon)

    print("\n🏁 Summary (lower is better):")
    if pkg:
        total_pkg = pkg["convert"] + pkg["transform"] + pkg["forecast"]
        print(f"   Package path total: {total_pkg:.3f}s  (convert={pkg['convert']:.3f}s, tf={pkg['transform']:.3f}s, fc={pkg['forecast']:.3f}s, numba={pkg['numba']})")
    if ps:
        total_ps = ps["transform"] + ps["forecast"]
        print(f"   pandas-on-Spark total: {total_ps:.3f}s (tf={ps['transform']:.3f}s, fc={ps['forecast']:.3f}s)")

    print("\n📌 When package+Numba is better:")
    print("   • Compute-heavy transforms and iterative loops per entity")
    print("   • Horizon is large (dozens), tight recurrence relations")
    print("   • Data fits on driver; conversion cost amortized")
    print("\n📌 When pandas-on-Spark is better:")
    print("   • Data larger-than-memory; need distributed execution")
    print("   • Group/window operations without tight per-row recurrences")
    print("   • You want to avoid driver collection and package distribution")

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



#!/usr/bin/env python3
"""
Frameworks: Stepwise optimizations for model scoring (impact breakdown)
======================================================================

Context: Builds directly on 06 (baseline). We take the same scoring task
and apply one optimization at a time, measuring the impact so teams can
decide which changes matter.

Optimizations covered (built on 06 baseline: Arrow→pandas→NumPy/Numba):
1) Column projection (reduce width before Arrow conversion)
2) Dtype tuning (float64 → float32)
3) JIT warmup/caching (amortize compilation)
4) Thread controls (avoid oversubscription)
5) Spark knobs (Arrow batch, shuffle partitions)

We reuse kernels from utils/modelpkg.py and generate a markdown report.
"""

from __future__ import annotations

import os
import sys
import time
import numpy as np

# Ensure utils importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.mem import get_total_memory_gb
from utils.modelpkg import transform_features, iterative_forecast

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col
from pyspark.sql import DataFrame


def build_base(spark: SparkSession, rows: int, entities: int, wide_cols: int = 0) -> DataFrame:
    from pyspark.sql.window import Window
    base = spark.range(rows).select(
        (col("id") % entities).alias("entity_id"),
        col("id").alias("t"),
        (F.rand() * 100.0).alias("values"),
        (F.rand() * 50.0 + 10.0).alias("prices"),
        (F.rand() > 0.5).cast("int").alias("flag"),
        (F.rand() * 5).cast("int").alias("cat"),
    )
    if wide_cols > 0:
        for i in range(wide_cols):
            base = base.withColumn(f"w_{i}", F.rand())
    # Keep schema simple; ordering applied later where needed
    return base


def _package_run(pdf, horizon: int, use_float32: bool) -> tuple[float, float]:
    # Returns (transform_s, forecast_s)
    t1 = time.time()
    vals = pdf["values"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
    prs = pdf["prices"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
    flag = pdf["flag"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
    cat = pdf["cat"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
    exog = np.stack([flag.astype(np.float64), cat.astype(np.float64)], axis=1)
    base = transform_features(vals.astype(np.float64), prs.astype(np.float64), exog)
    t_tf = time.time() - t1
    t2 = time.time()
    _ = iterative_forecast(pdf["entity_id"].to_numpy(dtype=np.int64, copy=False), base, horizon=horizon, alpha=0.3, beta=0.6)
    t_fc = time.time() - t2
    return t_tf, t_fc


def step0_baseline_package(spark: SparkSession, df: DataFrame, horizon: int, include_wide: bool, use_float32: bool) -> float:
    # Arrow → pandas conversion (slim vs wide), then NumPy/Numba kernels
    cols = ["entity_id", "values", "prices", "flag", "cat"]
    if include_wide:
        cols = df.columns  # convert all
    t0 = time.time()
    pdf = df.select(*cols).toPandas()
    t_conv = time.time() - t0
    t_tf, t_fc = _package_run(pdf, horizon, use_float32=use_float32)
    total = t_conv + t_tf + t_fc
    print(f"   convert: {t_conv:.3f}s | transform: {t_tf:.3f}s | forecast: {t_fc:.3f}s | total: {total:.3f}s")
    return total


def step1_projection(df: DataFrame) -> DataFrame:
    return df.select("entity_id", "t", "values", "prices", "flag", "cat")


def step2_partition_sort(df: DataFrame) -> DataFrame:
    # Kept for completeness if teams want a Spark-native path; not used in package baseline
    return df.repartition("entity_id").sortWithinPartitions("entity_id", "t")


def step3_grouped_pandas_udf(spark: SparkSession, df: DataFrame, horizon: int, use_float32: bool) -> float:
    # Grouped map pandas UDF: process each entity group as a pandas DataFrame
    # Requires Arrow enabled
    import pandas as pd
    from pyspark.sql.types import StructType, StructField, LongType, DoubleType
    from pyspark.sql.functions import pandas_udf, PandasUDFType

    # Control threads to avoid oversubscription
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    schema = StructType(
        [
            StructField("entity_id", LongType(), False),
            StructField("t", LongType(), False),
            StructField("y", DoubleType(), False),
        ]
    )

    @pandas_udf(schema, PandasUDFType.GROUPED_MAP)
    def score_group(pdf: pd.DataFrame) -> pd.DataFrame:
        vals = pdf["values"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
        prs = pdf["prices"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
        flag = pdf["flag"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
        cat = pdf["cat"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False)
        exog = np.stack([flag.astype(np.float64), cat.astype(np.float64)], axis=1)
        base = transform_features(vals.astype(np.float64), prs.astype(np.float64), exog)
        y = iterative_forecast(pdf["entity_id"].to_numpy(dtype=np.int64, copy=False), base, horizon=horizon, alpha=0.3, beta=0.6)
        out = pd.DataFrame({"entity_id": pdf["entity_id"].values, "t": pdf["t"].values, "y": y})
        return out

    t0 = time.time()
    sdf = df.groupBy("entity_id").apply(score_group)
    _ = sdf.select(F.avg("y")).collect()
    return time.time() - t0


def main():
    print("🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)")
    print("📚 Docs index: docs/index.md")
    mem = get_total_memory_gb()
    print(f"💻 System memory: {mem:.1f} GB")

    # Config tuned for Arrow batches and moderate shuffle
    spark = (
        SparkSession.builder.appName("Optimizations-07-Stepwise")
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.sql.execution.arrow.maxRecordsPerBatch", "2000")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.debug.maxToStringFields", "2000")
        .getOrCreate()
    )
    # Reduce noisy WARNs in local runs
    spark.sparkContext.setLogLevel("ERROR")

    # Dataset knobs
    rows, entities, horizon, wide = 600_000, 1_000, 36, 100
    print(f"rows={rows:,}, entities={entities:,}, horizon={horizon}, wide={wide}")

    base = build_base(spark, rows=rows, entities=entities, wide_cols=wide).cache()
    _ = base.count()

    # Baseline: package path (Arrow→pandas→NumPy/Numba), slim, float64
    print("\n== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==")
    t_base = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=False)

    # Step 1: demonstrate projection impact (convert full width)
    print("\n== Step 1: Projection (convert all wide columns vs slim) ==")
    t_full = step0_baseline_package(spark, base, horizon, include_wide=True, use_float32=False)
    print(f"   Δ vs baseline (slim): {t_full - t_base:+.3f}s")

    # Step 2: dtype tuning to float32
    print("\n== Step 2: Dtype tuning (float32 compute) ==")
    t_f32 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    print(f"   Δ vs baseline (f64): {t_f32 - t_base:+.3f}s")

    # Step 3: JIT warmup/caching (second run faster)
    print("\n== Step 3: JIT warmup (second run) ==")
    t_warm1 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    t_warm2 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    print(f"   first: {t_warm1:.3f}s | second: {t_warm2:.3f}s | Δ: {t_warm2 - t_warm1:+.3f}s")

    # Step 4: threads control (avoid oversubscription)
    print("\n== Step 4: Threads control (OMP/MKL) ==")
    os.environ["OMP_NUM_THREADS"] = "1"; os.environ["MKL_NUM_THREADS"] = "1"
    t_thr1 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    os.environ["OMP_NUM_THREADS"] = "4"; os.environ["MKL_NUM_THREADS"] = "4"
    t_thr4 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    print(f"   1-thread: {t_thr1:.3f}s | 4-threads: {t_thr4:.3f}s | Δ: {t_thr4 - t_thr1:+.3f}s")

    # Summary
    print("\n🏁 Summary (lower is better):")
    print(f"   Baseline (naive):   {t_base:.3f}s")
    print(f"   Step 1 (full width): {t_full:.3f}s")
    print(f"   Step 2 (float32):    {t_f32:.3f}s")
    print(f"   Step 3 (warm 2nd):   {t_warm2:.3f}s")
    print(f"   Step 4 (thr ctrl):   {min(t_thr1, t_thr4):.3f}s")

    spark.stop()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/07_optimizations_stepwise.md",
            title="Frameworks: Stepwise optimizations for model scoring",
            main_callable=main,
        )
    else:
        main()



#!/usr/bin/env python3
"""
Frameworks: Stepwise optimizations for model scoring (impact breakdown)
======================================================================

Context: Builds directly on 06 (baseline). We take the same scoring task
and apply one optimization at a time, measuring the impact so teams can
decide which changes matter.

Optimizations covered (built on 06 baseline: Arrow→pandas→NumPy/Numba):
1) Column projection (assumed best practice: reduce width before Arrow conversion)
2) Dtype tuning (float64 → float32)
3) Repartition by entity + streaming mapInPandas with fused kernel
4) Approximate sigmoid math (tanh-based)

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


def step2_streaming_map_in_pandas(spark: SparkSession, df: DataFrame, horizon: int, use_float32: bool, approx_sigmoid: bool = False) -> float:
    # Repartition by entity so all rows for an entity are in one partition
    sdf = df.repartition("entity_id").sortWithinPartitions("entity_id", "t")

    import pandas as pd
    from pyspark.sql.types import StructType, StructField, LongType, DoubleType

    schema = StructType([
        StructField("entity_id", LongType(), False),
        StructField("t", LongType(), False),
        StructField("y", DoubleType(), False),
    ])

    try:
        from numba import njit
        NUMBA = True
    except Exception:
        NUMBA = False

    def _sigmoid_np(x: np.ndarray) -> np.ndarray:
        if approx_sigmoid:
            # tanh approximation: sigmoid(x) ≈ 0.5 * (1 + tanh(0.5x))
            return 0.5 * (1.0 + np.tanh(0.5 * x))
        return 1.0 / (1.0 + np.exp(-x))

    if NUMBA:
        from numba import njit

        @njit(fastmath=True)
        def fused_kernel(values, prices, flag, cat, entity, horizon, alpha, beta):
            n = values.shape[0]
            y = np.empty(n, dtype=np.float64)
            last_e = -1
            state = 0.0
            for i in range(n):
                e = int(entity[i])
                if e != last_e:
                    last_e = e
                    state = 0.0
                tv = 0.15 * (values[i] * prices[i])
                sv = 0.07 * (values[i] ** 0.5)
                pr = 0.03 * (prices[i] ** 1.5)
                fv = 0.10 * (flag[i] * values[i])
                cv = 0.02 * (cat[i] * prices[i])
                base = tv + sv + pr + fv + cv
                local = state
                for _ in range(horizon):
                    # Use exact sigmoid for stability inside JIT
                    local = 1.0 / (1.0 + np.exp(-(alpha * base + beta * local)))
                y[i] = local
                state = 1.0 / (1.0 + np.exp(-(alpha * base + beta * state)))
            return y

    def _process_partition(pdf_iter):
        for pdf in pdf_iter:
            # Ensure per-partition contiguous entities
            pdf = pdf.sort_values(["entity_id", "t"], kind="mergesort")
            vals = pdf["values"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False).astype(np.float64)
            prs = pdf["prices"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False).astype(np.float64)
            flag = pdf["flag"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False).astype(np.float64)
            cat = pdf["cat"].to_numpy(dtype=np.float32 if use_float32 else np.float64, copy=False).astype(np.float64)
            ent = pdf["entity_id"].to_numpy(dtype=np.int64, copy=False)
            if NUMBA:
                y = fused_kernel(vals, prs, flag, cat, ent, horizon, 0.3, 0.6)
            else:
                # Fallback: vectorized features + python loop for forecast
                base = (
                    0.15 * (vals * prs)
                    + 0.07 * (vals ** 0.5)
                    + 0.03 * (prs ** 1.5)
                    + 0.10 * (flag * vals)
                    + 0.02 * (cat * prs)
                )
                y = np.empty_like(base)
                last = None
                state = 0.0
                for i in range(base.shape[0]):
                    if last is None or ent[i] != last:
                        state = 0.0
                        last = ent[i]
                    local = state
                    for _ in range(horizon):
                        local = _sigmoid_np(alpha=0.3 * base[i] + 0.6 * local)  # type: ignore
                    y[i] = local
                    state = _sigmoid_np(0.3 * base[i] + 0.6 * state)
            yield pd.DataFrame({"entity_id": pdf["entity_id"], "t": pdf["t"], "y": y})

    t0 = time.time()
    out = sdf.mapInPandas(_process_partition, schema)
    _ = out.select(F.avg("y")).collect()
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

    # Note: Projection of needed columns only is assumed from the baseline onward.
    # Avoid converting unused wide columns before Arrow → pandas.
    print("\nℹ️  Projection is assumed: converting only needed columns (avoid full width).")

    # Step 2: dtype tuning to float32 (baseline path)
    print("\n== Step 2: Dtype tuning (float32 compute on Arrow→pandas path) ==")
    t_f32 = step0_baseline_package(spark, step1_projection(base), horizon, include_wide=False, use_float32=True)
    print(f"   Δ vs baseline (float64): {t_f32 - t_base:+.3f}s")

    # Step 3: streaming iterator UDF (mapInPandas), fused kernel
    print("\n== Step 3: Repartition by entity + mapInPandas (fused kernel) ==")
    t_stream = step2_streaming_map_in_pandas(spark, step1_projection(base), horizon, use_float32=True, approx_sigmoid=False)
    print(f"   Δ vs baseline: {t_stream - t_base:+.3f}s")

    # Step 4: approximate sigmoid (faster math)
    print("\n== Step 4: Approximate sigmoid (tanh-based) in fused kernel ==")
    t_stream_approx = step2_streaming_map_in_pandas(spark, step1_projection(base), horizon, use_float32=True, approx_sigmoid=True)
    print(f"   Δ vs step3: {t_stream_approx - t_stream:+.3f}s")

    # Summary
    print("\n🏁 Summary (lower is better):")
    print(f"   Baseline (slim):     {t_base:.3f}s")
    print(f"   Step 2 (float32):    {t_f32:.3f}s")
    print(f"   Step 3 (stream):     {t_stream:.3f}s")
    print(f"   Step 4 (approx σ):   {t_stream_approx:.3f}s")

    print("\n📌 Guidance on streaming (mapInPandas):")
    print("   • Streaming keeps work distributed and avoids collecting to the driver.")
    print("   • In small local runs, overhead (repartition, Arrow batches, per-partition pandas frames, per-executor JIT warmup)")
    print("     can outweigh compute, so it may appear slower in this benchmark.")
    print("   • Enable it when: per-entity series are long, horizon is large, driver memory is tight, or end-to-end distribution is required.")
    print("   • If used, cache the repartitioned data, warm JIT once per executor, right-size partitions (≈2–3× cores), and limit OMP/MKL threads.")

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



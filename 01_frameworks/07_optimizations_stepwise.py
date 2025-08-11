#!/usr/bin/env python3
"""
Frameworks: Stepwise optimizations for model scoring (impact breakdown)
======================================================================

Context: Builds directly on 06 (baseline). We take the same scoring task
and apply one optimization at a time, measuring the impact so teams can
decide which changes matter.

Optimizations covered:
1) Column projection (reduce width)
2) Partitioning by entity_id and ordering within partition
3) Switch from naive Spark loops to grouped Pandas UDF with Arrow (per-entity)
4) Tune Arrow batch size and Spark shuffle partitions
5) Kernel/dtype tuning (float32), JIT warmup and threads control

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


def step0_naive_spark_loops(df: DataFrame, horizon: int) -> float:
    t0 = time.time()
    sdf = df.select("entity_id", "t", "values", "prices", "flag", "cat")
    sdf = sdf.withColumn(
        "feat",
        0.15 * (col("values") * col("prices"))
        + 0.07 * (col("values") ** F.lit(0.5))
        + 0.03 * (col("prices") ** F.lit(1.5))
        + 0.10 * (col("flag").cast("double") * col("values"))
        + 0.02 * (col("cat").cast("double") * col("prices")),
    )
    _ = sdf.select(F.avg("feat")).collect()
    sdf = sdf.withColumn("y", F.lit(0.0))
    for _ in range(horizon):
        sdf = sdf.withColumn("y", 1.0 / (1.0 + F.exp(-(0.3 * col("feat") + 0.6 * col("y")))))
    _ = sdf.select(F.avg("y")).collect()
    return time.time() - t0


def step1_projection(df: DataFrame) -> DataFrame:
    return df.select("entity_id", "t", "values", "prices", "flag", "cat")


def step2_partition_sort(df: DataFrame) -> DataFrame:
    # Hash partition by entity and preserve order for better locality
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
    print("🚀 Stepwise optimization experiment")
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

    # Baseline
    print("\n== Baseline: naive Spark with iterative withColumn loops ==")
    t_base = step0_naive_spark_loops(base, horizon)
    print(f"   time: {t_base:.3f}s")

    # Step 1: projection
    print("\n== Step 1: Project needed columns early ==")
    proj = step1_projection(base).cache(); _ = proj.count()
    t_proj = step0_naive_spark_loops(proj, horizon)
    print(f"   time: {t_proj:.3f}s  (delta vs baseline: {t_proj - t_base:+.3f}s)")

    # Step 2: partitioning and order
    print("\n== Step 2: Repartition by entity_id and sort within partitions ==")
    part = step2_partition_sort(proj).cache(); _ = part.count()
    t_part = step0_naive_spark_loops(part, horizon)
    print(f"   time: {t_part:.3f}s  (delta vs step1: {t_part - t_proj:+.3f}s)")

    # Step 3a: grouped pandas UDF (float64)
    print("\n== Step 3a: Grouped Pandas UDF per entity (float64) with Arrow ==")
    t_gp64 = step3_grouped_pandas_udf(spark, part, horizon, use_float32=False)
    print(f"   time: {t_gp64:.3f}s  (delta vs step2: {t_gp64 - t_part:+.3f}s)")

    # Step 3b: grouped pandas UDF (float32)
    print("\n== Step 3b: Grouped Pandas UDF per entity (float32) with Arrow ==")
    t_gp32 = step3_grouped_pandas_udf(spark, part, horizon, use_float32=True)
    print(f"   time: {t_gp32:.3f}s  (delta vs 3a: {t_gp32 - t_gp64:+.3f}s)")

    # Summary
    print("\n🏁 Summary (lower is better):")
    print(f"   Baseline (naive):   {t_base:.3f}s")
    print(f"   Step 1 (project):  {t_proj:.3f}s")
    print(f"   Step 2 (partition):{t_part:.3f}s")
    print(f"   Step 3a (gp udf64):{t_gp64:.3f}s")
    print(f"   Step 3b (gp udf32):{t_gp32:.3f}s")

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



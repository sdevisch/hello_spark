#!/usr/bin/env python3
"""
withColumn vs select: chaining cost, Arrow impact, and memory
============================================================

This script compares compute performance of:
- Chained `.withColumn` transformations
- A single `.select` projection expressing the same logic

We measure wall-clock time for a JVM-only action (`.count()`), so Arrow does not play a
role here. Arrow can speed up DataFrame → pandas conversion (e.g., `toPandas()`), but it
does not change withColumn/select execution inside the JVM.

Configure data size via `SIZES` (e.g., `SIZES=500k,1m,2m`) and complexity via
`DERIVED_COLS` (number of derived columns to build; default locked to 200). The benchmark times a
materializing aggregation that depends on the last derived column
(`agg(sum(cN))`) to ensure the transformations execute. Example:

- FAST run: `FAST=1 DERIVED_COLS=20 python 02_performance/03_withcolumn_vs_select.py`
- Full run: `DERIVED_COLS=40 SIZES=1m,2m python 02_performance/03_withcolumn_vs_select.py`
"""

from __future__ import annotations

import os
import time
import tempfile
import shutil
from typing import Callable, List
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, when


class WithColumnVsSelectBenchmark:
    def __init__(self, app_name: str = "WithColumnVsSelectBenchmark") -> None:
        compression = os.environ.get("PARQUET_COMPRESSION", "uncompressed")
        driver_mem = os.environ.get("SPARK_DRIVER_MEMORY", "4g")
        exec_mem = os.environ.get("SPARK_EXECUTOR_MEMORY", driver_mem)
        max_part_bytes = os.environ.get("SPARK_SQL_FILES_MAX_PARTITION_BYTES", "16m")
        self.spark = (
            SparkSession.builder.appName(app_name)
            .master("local[*]")
            # Keep Arrow default; we toggle per scenario
            .config("spark.sql.adaptive.enabled", "false")
            .config("spark.sql.shuffle.partitions", "200")
            .config("spark.sql.parquet.compression.codec", compression)
            .config("spark.driver.memory", driver_mem)
            .config("spark.executor.memory", exec_mem)
            .config("spark.sql.files.maxPartitionBytes", max_part_bytes)
            .getOrCreate()
        )
        self.spark.sparkContext.setLogLevel("WARN")
        # Default to a moderately complex chain; override with DERIVED_COLS
        # Lock in higher default complexity (can still override with DERIVED_COLS)
        try:
            self.num_derived_cols = int(os.environ.get("DERIVED_COLS", "200"))
        except ValueError:
            self.num_derived_cols = 200

    def _generate_df(self, num_rows: int) -> DataFrame:
        df = self.spark.range(num_rows).select(
            col("id"),
            (col("id") % 100).alias("a"),
            (col("id") % 50).alias("b"),
        )
        return df

    def _withcolumn_chain(self, df: DataFrame) -> DataFrame:
        """Apply a series of dependent column transformations using withColumn.

        The transformation pattern cycles through a small set of arithmetic/conditional
        expressions and builds columns c1..cN, each depending on the previous.
        """
        result = df
        a_col, b_col = col("a"), col("b")
        prev_name = None
        created_names: list[str] = []
        for step in range(1, self.num_derived_cols + 1):
            phase = (step - 1) % 7
            name = f"c{step}"
            if phase == 0:
                expr = a_col * 2 + 1
            elif phase == 1:
                expr = b_col * col(prev_name)
            elif phase == 2:
                expr = when(col(prev_name) % 3 == 0, col(prev_name) + 7).otherwise(col(prev_name) - 7)
            elif phase == 3:
                expr = col(prev_name) * 3 + a_col
            elif phase == 4:
                expr = col(prev_name) - b_col
            elif phase == 5:
                expr = col(prev_name) * 2
            else:
                # Avoid tiny cardinality (mod) that leads to tiny outputs and unrealistic timings
                expr = col(prev_name) * 31 + lit(7)
            result = result.withColumn(name, expr)
            created_names.append(name)
            prev_name = name
        return result.select("id", "a", "b", *created_names)

    def _select_combined(self, df: DataFrame) -> DataFrame:
        """Compute the same chain via a single select expression block.

        Builds c1..cN as expressions reusing the previous expression (not column name).
        """
        a_col, b_col = col("a"), col("b")
        prev_expr = None
        exprs: list = []
        for step in range(1, self.num_derived_cols + 1):
            phase = (step - 1) % 7
            if phase == 0:
                expr = a_col * 2 + 1
            elif phase == 1:
                expr = b_col * prev_expr
            elif phase == 2:
                expr = when(prev_expr % 3 == 0, prev_expr + 7).otherwise(prev_expr - 7)
            elif phase == 3:
                expr = prev_expr * 3 + a_col
            elif phase == 4:
                expr = prev_expr - b_col
            elif phase == 5:
                expr = prev_expr * 2
            else:
                # Avoid tiny cardinality (mod)
                expr = prev_expr * 31 + lit(7)
            exprs.append(expr.alias(f"c{step}"))
            prev_expr = expr
        return df.select("id", "a", "b", *exprs)

    def _measure_sum(self, label: str, df_fn: Callable[[DataFrame], DataFrame], rows: int) -> float:
        base_df = self._generate_df(rows)
        out_df = df_fn(base_df)
        # Ensure sufficient parallelism
        # Lock in higher parallelism by default (override with PARTITIONS if needed)
        try:
            target_parts = int(os.environ.get("PARTITIONS", "400"))
        except ValueError:
            target_parts = 400
        no_shuffle = os.environ.get("NO_SHUFFLE", "1") == "1"
        current_parts = out_df.rdd.getNumPartitions()
        if not no_shuffle and target_parts < current_parts:
            # Coalesce down without shuffle
            out_df = out_df.coalesce(target_parts)
        elif not no_shuffle and target_parts > current_parts:
            # Increasing partitions requires shuffle; skip if NO_SHUFFLE=1 (default)
            out_df = out_df.repartition(target_parts)
        last_col = f"c{self.num_derived_cols}"

        # Force full materialization by writing derived column to disk, then summing
        tmp_dir = tempfile.mkdtemp()
        try:
            write_path = os.path.join(tmp_dir, "out.parquet")
            t0 = time.time()
            out_df.select(F.col(last_col)).write.option("compression", os.environ.get("PARQUET_COMPRESSION", "uncompressed")).mode("overwrite").parquet(write_path)
            t1 = time.time()
            total1 = t1 - t0
            # Measure bytes written
            total_bytes = 0
            for root, _dirs, files in os.walk(write_path):
                for fn in files:
                    fp = os.path.join(root, fn)
                    try:
                        total_bytes += os.path.getsize(fp)
                    except OSError:
                        pass
            mb = total_bytes / (1024 * 1024)

            t2 = time.time()
            _ = self.spark.read.parquet(write_path).agg(F.sum(F.col(last_col))).collect()
            t3 = time.time()
            total2 = t3 - t2

            total = total1 + total2
            print(f"{label} | rows={rows:,} | parts={target_parts} | bytes≈{mb:.1f}MB | write={total1:.2f}s | sum(read)={total2:.2f}s | total={total:.2f}s")
            return total
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def run_multiple(self, row_sizes: List[int]) -> None:
        print("\n=== withColumn vs select: JVM compute (agg sum of last column) ===")
        print(f"Spark version: {self.spark.version}")
        print(f"Row sizes: {[format(s, ',') for s in row_sizes]}")
        print(f"Derived columns: {self.num_derived_cols}")
        for rows in row_sizes:
            print(f"\n--- Running scenarios for rows={rows:,} ---")
            t_with = self._measure_sum("withColumn_chain", self._withcolumn_chain, rows)
            t_sel = self._measure_sum("select_combined", self._select_combined, rows)
            speedup = (t_with / t_sel) if t_sel > 0 else float('inf')
            print(f"Summary | rows={rows:,} | withColumn_chain={t_with:.2f}s | select_combined={t_sel:.2f}s | speedup={speedup:.1f}x")
        print("\nWhy select can be faster here:")
        print("- select composes one expression tree for all derived columns, so Catalyst/codegen emits a single, tight kernel.")
        print("- withColumn chaining introduces many intermediate aliases and Projects; the optimizer can fold them, but analysis/codegen overhead can be higher.")
        print("- Both compute in the JVM. Differences mainly come from expression composition, plan size, and codegen, not from Arrow or Python.")
        print("\nDone.")


def _parse_sizes_from_env(default_sizes: List[int]) -> List[int]:
    raw = os.environ.get("SIZES")
    if not raw:
        return default_sizes
    sizes: List[int] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            if token.lower().endswith("k"):
                sizes.append(int(float(token[:-1]) * 1_000))
            elif token.lower().endswith("m"):
                sizes.append(int(float(token[:-1]) * 1_000_000))
            else:
                sizes.append(int(float(token)))
        except ValueError:
            continue
    return sizes or default_sizes


def main() -> None:
    fast = os.environ.get("FAST", "0") == "1"
    # FAST defaults vs full defaults (10x scale-up)
    default_sizes = [1_000_000, 3_000_000] if fast else [5_000_000, 10_000_000, 20_000_000]
    sizes = _parse_sizes_from_env(default_sizes)
    bench = WithColumnVsSelectBenchmark()
    try:
        bench.run_multiple(sizes)
    finally:
        bench.spark.stop()


if __name__ == "__main__":
    import os as _os
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/perf_03_withcolumn_vs_select.md",
            title="Performance 03: withColumn vs select (JVM compute only)",
            main_callable=main,
        )
    else:
        main()



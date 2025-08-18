#!/usr/bin/env python3
"""
withColumn vs select: JVM compute comparison only
=================================================

Clean, reproducible comparison of:
- Chained `.withColumn` transformations
- A single `.select` projection expressing the same logic

Measured using a JVM-only action that depends on the final derived column
(aggregate sum), so all transformations execute. No pandas/Arrow involved.
"""

from __future__ import annotations

import os
import time
from typing import Callable
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, when


class WithColumnVsSelectBenchmark:
    def __init__(self, app_name: str = "WithColumnVsSelectBenchmark") -> None:
        self.spark = SparkSession.builder.appName(app_name).master("local[*]").getOrCreate()
        self.spark.sparkContext.setLogLevel("WARN")

    def _generate_df(self, num_rows: int) -> DataFrame:
        df = self.spark.range(num_rows).select(
            col("id"),
            (col("id") % 100).alias("a"),
            (col("id") % 50).alias("b"),
        )
        return df

    def _withcolumn_chain(self, df: DataFrame) -> DataFrame:
        result = df
        result = result.withColumn("c", col("a") * 2 + 1)
        result = result.withColumn("d", col("b") * col("c"))
        result = result.withColumn("e", when(col("d") % 3 == 0, col("d") + 7).otherwise(col("d") - 7))
        result = result.withColumn("f", col("e") * 3 + col("a"))
        result = result.withColumn("g", col("f") - col("b"))
        result = result.withColumn("h", col("g") * 2)
        result = result.withColumn("i", col("h") + lit(42))
        result = result.withColumn("j", col("i") * 31 + lit(7))
        return result.select("id", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j")

    def _select_combined(self, df: DataFrame) -> DataFrame:
        c = (col("a") * 2 + 1).alias("c")
        d = (col("b") * (col("a") * 2 + 1)).alias("d")
        e = when(d % 3 == 0, d + 7).otherwise(d - 7).alias("e")
        f = (e * 3 + col("a")).alias("f")
        g = (f - col("b")).alias("g")
        h = (g * 2).alias("h")
        i = (h + lit(42)).alias("i")
        j = (i * 31 + lit(7)).alias("j")
        return df.select("id", "a", "b", c, d, e, f, g, h, i, j)

    def _measure(self, label: str, df_fn: Callable[[DataFrame], DataFrame], rows: int) -> float:
        base_df = self._generate_df(rows)
        df = df_fn(base_df)
        start = time.time()
        _ = df.agg(F.sum(F.col("j"))).collect()
        elapsed = time.time() - start
        print(f"{label} | rows={rows:,} | action=sum(j) | time={elapsed:.2f}s")
        return elapsed

    def run_multiple(self, row_sizes: List[int]) -> None:
        print("\n=== withColumn vs select: JVM compute (agg sum of last column) ===")
        print(f"Spark version: {self.spark.version}")
        print(f"Row sizes: {[format(s, ',') for s in row_sizes]}")
        for rows in row_sizes:
            print(f"\n--- Running scenarios for rows={rows:,} ---")
            t_with = self._measure("withColumn_chain", self._withcolumn_chain, rows)
            t_sel = self._measure("select_combined", self._select_combined, rows)
            speedup = (t_with / t_sel) if t_sel > 0 else float('inf')
            print(f"Summary | rows={rows:,} | withColumn_chain={t_with:.2f}s | select_combined={t_sel:.2f}s | speedup={speedup:.1f}x")
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
    # FAST defaults vs full defaults
    default_sizes = [100_000, 300_000] if fast else [500_000, 1_000_000, 2_000_000]
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



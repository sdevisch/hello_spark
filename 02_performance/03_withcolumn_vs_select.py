#!/usr/bin/env python3
"""
withColumn vs select: chaining cost, Arrow impact, and memory
============================================================

This script compares performance and memory usage for:
- Chained .withColumn transformations ending with toPandas()
- The same logic expressed via a single .select() call

Each scenario is measured with Arrow disabled and enabled where relevant.
We report wall-clock time and driver RSS memory delta for a rough comparison.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import psutil
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, when


@dataclass
class ScenarioResult:
    name: str
    arrow_enabled: bool
    rows: int
    duration_seconds: float
    rss_delta_mb: float


class WithColumnVsSelectBenchmark:
    def __init__(self, app_name: str = "WithColumnVsSelectBenchmark") -> None:
        self.spark = (
            SparkSession.builder.appName(app_name)
            .master("local[*]")
            # Keep Arrow default; we toggle per scenario
            .config("spark.sql.adaptive.enabled", "true")
            .getOrCreate()
        )
        self.spark.sparkContext.setLogLevel("WARN")

    def _generate_df(self, num_rows: int) -> DataFrame:
        df = self.spark.range(num_rows).select(
            col("id"),
            (col("id") % 100).alias("a"),
            (col("id") % 50).alias("b"),
        )
        return df

    def _withcolumn_chain(self, df: DataFrame) -> DataFrame:
        # Apply a series of dependent column transformations
        result = df
        result = result.withColumn("c", col("a") * 2 + 1)
        result = result.withColumn("d", col("b") * col("c"))
        result = result.withColumn("e", when(col("d") % 3 == 0, col("d") + 7).otherwise(col("d") - 7))
        result = result.withColumn("f", (col("e") * 3 + col("a")).alias("f"))
        result = result.withColumn("g", (col("f") - col("b")).alias("g"))
        result = result.withColumn("h", (col("g") * 2).alias("h"))
        result = result.withColumn("i", (col("h") + lit(42)).alias("i"))
        result = result.withColumn("j", (col("i") % 97).alias("j"))
        return result.select("id", "a", "b", "c", "d", "e", "f", "g", "h", "j")

    def _select_combined(self, df: DataFrame) -> DataFrame:
        # Compute final columns using a single select expression block
        c = (col("a") * 2 + 1).alias("c")
        d = (col("b") * (col("a") * 2 + 1)).alias("d")
        e = when((col("b") * (col("a") * 2 + 1)) % 3 == 0, (col("b") * (col("a") * 2 + 1)) + 7).otherwise(
            (col("b") * (col("a") * 2 + 1)) - 7
        ).alias("e")
        f = (e * 3 + col("a")).alias("f")
        g = (f - col("b")).alias("g")
        h = (g * 2).alias("h")
        j = ((h + lit(42)) % 97).alias("j")
        return df.select("id", "a", "b", c, d, e, f, g, h, j)

    def _measure(self, name: str, arrow_enabled: bool, df_fn: Callable[[DataFrame], DataFrame], rows: int) -> ScenarioResult:
        # Toggle Arrow (affects toPandas)
        self.spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true" if arrow_enabled else "false")

        base_df = self._generate_df(rows)
        proc = psutil.Process(os.getpid())
        rss_before = proc.memory_info().rss
        start_time = time.time()

        # Force materialization by converting to pandas (to exercise Arrow) and summing a column
        pandas_df = df_fn(base_df).toPandas()
        _ = pandas_df["j"].sum()

        duration = time.time() - start_time
        rss_after = proc.memory_info().rss
        rss_delta_mb = (rss_after - rss_before) / (1024 * 1024)
        print(f"{name} | rows={rows:,} | arrow={arrow_enabled} | time={duration:.2f}s | rssΔ={rss_delta_mb:.2f}MB")
        return ScenarioResult(name=name, arrow_enabled=arrow_enabled, rows=rows, duration_seconds=duration, rss_delta_mb=rss_delta_mb)

    def run(self, rows: int) -> List[ScenarioResult]:
        print("\n=== withColumn vs select: performance and memory ===")
        print(f"Spark version: {self.spark.version}")
        print(f"Rows: {rows:,}")

        results: List[ScenarioResult] = []

        # 1) withColumn chain without Arrow
        results.append(self._measure("withColumn_chain -> toPandas", False, self._withcolumn_chain, rows))

        # 2) withColumn chain with Arrow
        results.append(self._measure("withColumn_chain -> toPandas", True, self._withcolumn_chain, rows))

        # 3) select-combined with Arrow
        results.append(self._measure("select_combined -> toPandas", True, self._select_combined, rows))

        # 4) Optional: select-combined without Arrow (for completeness)
        results.append(self._measure("select_combined -> toPandas", False, self._select_combined, rows))

        print("\nSummary:")
        print(f"{'Scenario':<32} {'Arrow':<7} {'Rows':>10} {'Time (s)':>10} {'RSS Δ (MB)':>12}")
        print("-" * 80)
        for r in results:
            print(f"{r.name:<32} {str(r.arrow_enabled):<7} {r.rows:>10,} {r.duration_seconds:>10.2f} {r.rss_delta_mb:>12.2f}")

        return results


def main() -> None:
    fast = os.environ.get("FAST", "0") == "1"
    # Keep FAST small to avoid long runs in CI/e2e
    rows = 100_000 if fast else 2_000_000
    bench = WithColumnVsSelectBenchmark()
    try:
        bench.run(rows)
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
            title="Performance 03: withColumn vs select (Arrow on/off, time and memory)",
            main_callable=main,
        )
    else:
        main()



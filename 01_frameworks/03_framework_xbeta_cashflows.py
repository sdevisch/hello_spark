#!/usr/bin/env python3
"""
Framework XBeta & Cashflows (appendix case study)
=================================================

This script builds a realistic panel (entities × days) dataset in Spark,
then compares computing:
- Feature vector f (5 features)
- Per-entity beta vector b (5 coefficients)
- Linear score xbeta = f · b
- Cash flow_t = revenue_t * sigmoid(xbeta_t)
- Rolling 30-day cash flow per entity (sliding window)

Frameworks compared (supporting the main guidance):
1. Spark (native, Window functions) — baseline
2. Pandas (groupby + rolling) — Arrow→pandas path
3. NumPy / Numba — niche rolling kernel illustration

Data starts in Spark; all conversions measure serialization costs.
"""

import os
import sys
import time
import numpy as np
import pandas as pd
# Ensure repo root for utils.*
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.mem import get_total_memory_gb, get_process_memory_mb
from typing import Dict, Tuple
import os as _os

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col
from pyspark.sql.window import Window

try:
    import numba
    from numba import njit
    NUMBA_AVAILABLE = True
except Exception:
    NUMBA_AVAILABLE = False


def fix_numpy_compatibility() -> None:
    os.environ.setdefault("PYARROW_IGNORE_TIMEZONE", "1")
    # Minimal compat for pandas-on-spark if needed elsewhere
    if not hasattr(np, "NaN") and hasattr(np, "nan"):
        np.NaN = np.nan  # type: ignore[attr-defined]


fix_numpy_compatibility()


class XbetaCashflowComparison:
    def __init__(self, rows: int = 200_000) -> None:
        self.rows = rows
        print("🔬 XBETAs & CASHFLOWS COMPARISON (panel data)")
        print("=" * 60)
        print(f"📊 Target rows (approx): {rows:,}")
        print("🎯 Data starts in Spark; we compare frameworks on xbeta & rolling sums")
        print("=" * 60)

        self.spark_no_arrow = (
            SparkSession.builder.appName("Xbeta-CF-NoArrow")
            .master("local[*]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "false")
            .getOrCreate()
        )
        self.spark_with_arrow = (
            SparkSession.builder.appName("Xbeta-CF-WithArrow")
            .master("local[*]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
        self.spark_no_arrow.sparkContext.setLogLevel("WARN")
        self.spark_with_arrow.sparkContext.setLogLevel("WARN")
        print("🌐 Spark UI: http://localhost:4040 (or 4041)")

    # -------- infra helpers --------
    def get_memory_usage(self) -> float:
        return get_process_memory_mb() / 1024.0

    def time_op(self, name: str, fn, *args, **kwargs) -> Tuple[object, float]:
        start_mem = self.get_memory_usage()
        print(f"⏱️  {name}")
        t0 = time.time()
        res = fn(*args, **kwargs)
        dt = time.time() - t0
        dmem = self.get_memory_usage() - start_mem
        print(f"   ✅ {dt:.4f}s | ΔMem {dmem:+.3f} GB")
        return res, dt

    # -------- data generation --------
    def create_panel_data(self) -> Tuple[object, int, int]:
        """Create panel data in Spark: entities × days ~= rows.
        Returns (spark_df, num_entities, num_days).
        """
        print("\n" + "=" * 60)
        print("📊 CREATING PANEL DATA IN SPARK (entities × days)")
        print("=" * 60)

        # Choose panel shape close to requested rows
        num_entities = max(50, min(2_000, self.rows // 200))
        num_days = max(30, self.rows // max(1, num_entities))
        print(f"   Entities: {num_entities:,} | Days: {num_days:,} | Target rows≈{num_entities*num_days:,}")

        def _build():
            spark = self.spark_with_arrow
            # Entities table with per-entity betas b1..b5
            entities = (
                spark.range(num_entities).select(
                    col("id").alias("entity_id"),
                    (F.rand() * 0.8 - 0.4).alias("b1"),
                    (F.rand() * 0.8 - 0.4).alias("b2"),
                    (F.rand() * 0.8 - 0.4).alias("b3"),
                    (F.rand() * 0.8 - 0.4).alias("b4"),
                    (F.rand() * 0.8 - 0.4).alias("b5"),
                    (F.rand() > 0.7).alias("is_premium"),
                    (F.rand() * 5).cast("int").alias("category"),
                )
            )
            days = self.spark_with_arrow.range(num_days).select(col("id").alias("day"))
            panel = entities.crossJoin(days)  # entity_id × day

            # Features as functions of day/entity
            panel = panel.select(
                "entity_id",
                "day",
                "b1",
                "b2",
                "b3",
                "b4",
                "b5",
                "is_premium",
                "category",
                (F.sin(col("day") / F.lit(7.0)) + (F.rand() - 0.5) * 0.1).alias("f1"),
                (F.cos(col("day") / F.lit(30.0)) + (F.rand() - 0.5) * 0.1).alias("f2"),
                ((F.rand() * 2 - 1) * (col("category") + 1)).alias("f3"),
                ((F.rand() * 0.5) + (col("is_premium").cast("int") * 0.3)).alias("f4"),
                (F.rand() * 1.5).alias("f5"),
                (F.rand() * 200 + 50).alias("revenue"),
            )

            # xbeta & cash_flow
            panel = panel.withColumn(
                "xbeta",
                col("f1") * col("b1")
                + col("f2") * col("b2")
                + col("f3") * col("b3")
                + col("f4") * col("b4")
                + col("f5") * col("b5"),
            )
            panel = panel.withColumn("sigmoid_xbeta", 1 / (1 + F.exp(-col("xbeta"))))
            panel = panel.withColumn("cash_flow", col("revenue") * col("sigmoid_xbeta"))

            # Rolling 30-day cash flow per entity
            w = Window.partitionBy("entity_id").orderBy(col("day").asc()).rowsBetween(-29, 0)
            panel = panel.withColumn("cf_30d", F.sum("cash_flow").over(w))

            return panel.cache()

        df, _ = self.time_op("Build Spark panel (with betas, features, xbeta, CF, rolling)", _build)
        cnt = df.count()
        print(f"   ✅ Materialized rows: {cnt:,}")
        return df, num_entities, num_days

    # -------- conversions --------
    def convert_to_pandas(self, df) -> pd.DataFrame:
        def _to_pd():
            return df.toPandas()
        pdf, _ = self.time_op("Convert Spark→pandas (Arrow)", _to_pd)
        return pdf

    def convert_to_pandas_both(self, df) -> Tuple[pd.DataFrame, float, pd.DataFrame, float]:
        """Return (pdf_arrow, t_arrow, pdf_no_arrow, t_no_arrow)."""
        def _arrow():
            return df.toPandas()
        pdf_arrow, t_arrow = self.time_op("Convert Spark→pandas (Arrow)", _arrow)

        def _no_arrow():
            # Force non-Arrow path by re-materializing into the no-arrow session
            df_no_arrow = self.spark_no_arrow.createDataFrame(df.collect())
            return df_no_arrow.toPandas()
        pdf_no_arrow, t_no_arrow = self.time_op("Convert Spark→pandas (No Arrow)", _no_arrow)

        return pdf_arrow, t_arrow, pdf_no_arrow, t_no_arrow

    def convert_to_numpy(self, pdf: pd.DataFrame, label: str = "") -> Tuple[Dict[str, np.ndarray], float]:
        def _to_np():
            # Ensure sort by entity/day for rolling
            pdf2 = pdf.sort_values(["entity_id", "day"]) \
                     .reset_index(drop=True)
            return {
                "entity_id": pdf2["entity_id"].values.astype(np.int64),
                "day": pdf2["day"].values.astype(np.int32),
                "f": pdf2[["f1", "f2", "f3", "f4", "f5"]].values.astype(np.float64),
                "b": pdf2[["b1", "b2", "b3", "b4", "b5"]].values.astype(np.float64),
                "revenue": pdf2["revenue"].values.astype(np.float64),
            }
        label_suffix = f" from {label}" if label else ""
        np_data, t_prep = self.time_op(f"Prepare NumPy arrays (sorted by entity/day){label_suffix}", _to_np)
        return np_data, t_prep

    # -------- computations --------
    def compute_spark(self, df):
        # Already computed xbeta and cf_30d in create step; re-run a lightweight agg
        def _run():
            return (
                df.groupBy("entity_id")
                .agg(F.avg("xbeta").alias("avg_xb"), F.avg("cf_30d").alias("avg_cf30"))
                .count()
            )
        _, t = self.time_op("Spark compute (reuse xbeta, CF rolling, entity agg)", _run)
        return t

    def compute_pandas(self, pdf: pd.DataFrame):
        def _run():
            pdf2 = pdf.sort_values(["entity_id", "day"]).copy()
            # xbeta already present; recompute cash flow and rolling to be fair
            pdf2["sigmoid_xbeta"] = 1.0 / (1.0 + np.exp(-pdf2["xbeta"]))
            pdf2["cash_flow"] = pdf2["revenue"] * pdf2["sigmoid_xbeta"]
            roll = (
                pdf2.groupby("entity_id")["cash_flow"].rolling(window=30, min_periods=1).sum()
            )
            pdf2["cf_30d"] = roll.reset_index(level=0, drop=True)
            return int(pdf2["cf_30d"].shape[0])
        _, t = self.time_op("Pandas compute (rolling per entity)", _run)
        return t

    @staticmethod
    @njit
    def _numba_rolling_sum_by_entity(entity_id: np.ndarray, values: np.ndarray, window: int = 30) -> np.ndarray:
        n = values.shape[0]
        out = np.empty(n, dtype=np.float64)
        # Simple circular buffer per entity
        buf = np.zeros(window, dtype=np.float64)
        buf_counts = np.zeros(window, dtype=np.int64)  # not strictly needed; kept for clarity
        head = 0
        current_entity = -1
        current_sum = 0.0
        filled = 0
        for i in range(n):
            e = int(entity_id[i])
            if e != current_entity:
                # reset
                current_entity = e
                head = 0
                current_sum = 0.0
                filled = 0
                for k in range(window):
                    buf[k] = 0.0
                    buf_counts[k] = 0
            # push
            current_sum -= buf[head]
            buf[head] = values[i]
            current_sum += buf[head]
            head += 1
            if head == window:
                head = 0
                filled = window
            else:
                if filled < window:
                    filled += 1
            out[i] = current_sum  # window sum with min_periods=1 semantics
        return out

    def compute_numpy_and_numba(self, np_data: Dict[str, np.ndarray]) -> Tuple[float, float]:
        def _numpy_part():
            xbeta = (np_data["f"] * np_data["b"]).sum(axis=1)
            sigmoid = 1.0 / (1.0 + np.exp(-xbeta))
            cash_flow = np_data["revenue"] * sigmoid
            return xbeta, cash_flow

        (xbeta, cash_flow), t_np = self.time_op("NumPy: xbeta + cash_flow (vectorized)", _numpy_part)

        t_numba = 0.0
        if NUMBA_AVAILABLE:
            # Warm-up JIT
            _ = self._numba_rolling_sum_by_entity(np_data["entity_id"][:100], cash_flow[:100], 30)

            def _numba_part():
                return self._numba_rolling_sum_by_entity(np_data["entity_id"], cash_flow, 30)

            _, t_numba = self.time_op("Numba: rolling 30d cash_flow per entity", _numba_part)
        else:
            print("⚠️ Numba not available; skipping JIT rolling computation")

        return t_np, t_numba

    # -------- orchestrator --------
    def run(self) -> None:
        try:
            spark_panel, n_entities, n_days = self.create_panel_data()

            t_spark = self.compute_spark(spark_panel)

            # Compare Arrow vs No-Arrow conversion
            pdf_arrow, t_arrow, pdf_no_arrow, t_no_arrow = self.convert_to_pandas_both(spark_panel)
            if t_arrow > 0:
                print(f"   🏹 Arrow speedup Spark→pandas: {t_no_arrow / t_arrow:.1f}x")

            # Use Arrow path for downstream single-machine comps
            pdf = pdf_arrow
            t_pandas = self.compute_pandas(pdf)

            np_data_arrow, t_np_prep_arrow = self.convert_to_numpy(pdf_arrow, label="pandas (Arrow)")
            # Also measure pandas→NumPy prep time for the no-Arrow DataFrame
            _, t_np_prep_no_arrow = self.convert_to_numpy(pdf_no_arrow, label="pandas (NoArrow)")

            t_numpy, t_numba = self.compute_numpy_and_numba(np_data_arrow)

            print("\n" + "=" * 60)
            print("🏁 RESULTS (wall times)")
            print("=" * 60)
            # Explain terminology
            print("🔎 Terminology:")
            print("   • Conversion: Spark→pandas with/without Arrow")
            print("   • Prep: pandas→NumPy array preparation (sorting, view extraction)")
            print("   • Compute only: pure algorithm time (no conversion/prep)")
            print("   • Total: conversion + prep + compute")

            # Conversions
            print("\n📦 Conversion timings:")
            print(f"   Spark→pandas (Arrow):   {t_arrow:.4f}s")
            print(f"   Spark→pandas (NoArrow): {t_no_arrow:.4f}s")
            print(f"   🏹 Arrow speedup:        {(t_no_arrow / t_arrow) if t_arrow else float('inf'):.1f}x")

            # Prep
            print("\n🧰 Prep timings (pandas→NumPy):")
            print(f"   From pandas (Arrow):    {t_np_prep_arrow:.4f}s")
            print(f"   From pandas (NoArrow):  {t_np_prep_no_arrow:.4f}s")

            # Compute-only
            print("\n⚙️  Compute-only timings:")
            print(f"   NumPy (xbeta + cf):     {t_numpy:.4f}s")
            if NUMBA_AVAILABLE:
                print(f"   Numba (rolling 30d):    {t_numba:.4f}s")
            else:
                print("   Numba (rolling 30d):    n/a")

            # Totals
            print("\n📈 End-to-end totals (conversion + prep + compute):")
            total_numpy_arrow = t_arrow + t_np_prep_arrow + t_numpy
            total_numpy_no_arrow = t_no_arrow + t_np_prep_no_arrow + t_numpy
            print(f"   NumPy total (Arrow):    {total_numpy_arrow:.4f}s")
            print(f"   NumPy total (NoArrow):  {total_numpy_no_arrow:.4f}s")

            if NUMBA_AVAILABLE:
                # Numba depends on NumPy xbeta+cf; include both in total
                total_numba_arrow = t_arrow + t_np_prep_arrow + t_numpy + t_numba
                total_numba_no_arrow = t_no_arrow + t_np_prep_no_arrow + t_numpy + t_numba
                print(f"   Numba total (Arrow):    {total_numba_arrow:.4f}s")
                print(f"   Numba total (NoArrow):  {total_numba_no_arrow:.4f}s")

            # Spark & Pandas standalone
            print("\n🖥️  In-framework compute-only:")
            print(f"   Spark (reuse/agg):      {t_spark:.4f}s")
            print(f"   Pandas (rolling):       {t_pandas:.4f}s")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n🧹 Cleaning up Spark...")
            self.spark_no_arrow.stop()
            self.spark_with_arrow.stop()
            print("   ✅ Done")


def main() -> None:
    print("🚀 Starting Xbeta & Cashflows Panel Comparison...")
    print("📚 Docs index: docs/index.md")
    memory_gb = get_total_memory_gb()
    print(f"💻 System memory: {memory_gb:.1f} GB")
    if memory_gb < 8:
        rows = 100_000
    elif memory_gb < 16:
        rows = 200_000
    else:
        rows = 300_000
    runner = XbetaCashflowComparison(rows=rows)
    runner.run()


if __name__ == "__main__":
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/03_framework_xbeta_cashflows.md",
            title="Frameworks: Panel xbeta & cashflows (appendix case)",
            main_callable=main,
        )
    else:
        main()

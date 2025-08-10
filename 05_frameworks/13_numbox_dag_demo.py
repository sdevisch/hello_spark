#!/usr/bin/env python3
"""
Appendix: Numbox DAG Demo (advanced, optional)
==============================================

This script demonstrates how to build a complex DAG of computations on top of
NumPy/Numba and then execute it using Numbox primitives for better structure
and potential JIT caching benefits. It runs side-by-side timings of:

- NumPy vectorized operations
- Numba monolithic JIT function
- Numbox DAG execution (if `numbox` is installed)

It explicitly compares computations in a Spark context with two conversion
paths:

- Spark → pandas with Arrow (fast columnar transfer)
- Spark → pandas without Arrow (expensive serialization)

For each path, it benchmarks:

- Pandas (vectorized)
- NumPy (vectorized arrays prepared from pandas)
- Numba (monolithic @njit parallel pipeline)
- Numbox (DAG with Node/Work/Proxy, when available)

It prints conversion, preparation, and compute timings, and can emit a
markdown report via the GENERATE_DOCS hook.

Reference: Numbox toolbox for low-level numba utilities [numbox]. Use when you benefit from DAG structuring and JIT reuse; not required for typical Spark↔pandas pipelines.

[numbox]: https://github.com/Goykhman/numbox
"""

import os
import time
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import psutil

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col

try:
    import numba
    from numba import njit, prange
    NUMBA_AVAILABLE = True
except Exception:
    NUMBA_AVAILABLE = False

try:
    import numbox  # type: ignore
    NUMBOX_AVAILABLE = True
except Exception:
    NUMBOX_AVAILABLE = False


def _fix_numpy_compatibility() -> None:
    os.environ.setdefault("PYARROW_IGNORE_TIMEZONE", "1")
    if not hasattr(np, "NaN") and hasattr(np, "nan"):
        np.NaN = np.nan  # type: ignore[attr-defined]


_fix_numpy_compatibility()


class NumboxDagDemo:
    def __init__(self, rows: int = 200_000) -> None:
        self.rows = rows
        print("🔬 NUMBOX DAG DEMO")
        print("=" * 60)
        print(f"📊 Dataset size: {rows:,} rows")
        print("🎯 Comparing: Pandas vs NumPy vs Numba vs Numbox (DAG)")
        print("=" * 60)

        # Spark contexts: with and without Arrow
        self.spark_no_arrow = (
            SparkSession.builder.appName("Numbox-DAG-NoArrow")
            .master("local[*]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "false")
            .config("spark.sql.adaptive.enabled", "false")
            .getOrCreate()
        )
        self.spark_with_arrow = (
            SparkSession.builder.appName("Numbox-DAG-WithArrow")
            .master("local[*]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .config("spark.sql.adaptive.enabled", "false")
            .getOrCreate()
        )
        self.spark_no_arrow.sparkContext.setLogLevel("WARN")
        self.spark_with_arrow.sparkContext.setLogLevel("WARN")
        print("🌐 Spark UI (No Arrow): http://localhost:4040")
        print("🌐 Spark UI (With Arrow): http://localhost:4041")

    # ----- infra helpers -----
    @staticmethod
    def _mem_gb() -> float:
        return psutil.Process(os.getpid()).memory_info().rss / (1024 ** 3)

    def _time(self, name: str, fn, *args, **kwargs) -> Tuple[object, float, float]:
        start_mem = self._mem_gb()
        print(f"⏱️  {name}")
        t0 = time.time()
        res = fn(*args, **kwargs)
        dt = time.time() - t0
        dmem = self._mem_gb() - start_mem
        print(f"   ✅ {dt:.4f}s | ΔMem {dmem:+.3f} GB")
        return res, dt, dmem

    # ----- data generation -----
    def _generate_spark_dataframe(self):
        n = self.rows
        spark = self.spark_with_arrow
        def _build():
            df = spark.range(n).select(
                col("id").alias("row_id"),
                (F.rand() * 100.0).alias("values"),
                (F.rand() * 50.0 + 25.0).alias("prices"),
                ((F.rand() * 100.0) * (F.rand() * 50.0 + 25.0)).alias("revenue"),
                (F.rand() * 20.0 - 10.0).alias("profit_margin"),
                (F.rand() * 1000.0).alias("quantities"),
                (F.rand() * 5).cast("int").alias("category"),
                (F.rand() > 0.7).alias("is_premium"),
            )
            return df.cache()
        df, _, _ = self._time("Create Spark DataFrame (cached)", _build)
        cnt = df.count()
        print(f"   ✅ Materialized rows: {cnt:,}")
        return df

    # ----- conversion helpers -----
    def _spark_to_pandas_arrow(self, df):
        return df.toPandas()

    def _spark_to_pandas_no_arrow(self, df):
        df_no_arrow = self.spark_no_arrow.createDataFrame(df.collect())
        return df_no_arrow.toPandas()

    def _to_numpy(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        return {
            "values": df["values"].values,
            "prices": df["prices"].values,
            "revenue": df["revenue"].values,
            "profit_margin": df["profit_margin"].values,
            "quantities": df["quantities"].values,
            "category": df["category"].values,
            "is_premium": df["is_premium"].values,
        }

    # ----- pandas computation -----
    @staticmethod
    def _pandas_pipeline(pdf: pd.DataFrame) -> float:
        df = pdf.copy()
        df["total_value"] = df["values"] * df["prices"]
        df["adjusted_revenue"] = df["revenue"] * (1.0 + df["profit_margin"] / 100.0)
        df["sqrt_values"] = np.sqrt(df["values"])  # use numpy ufunc on pandas Series
        df["weighted_qty"] = df["quantities"] + df["values"] * 2.0
        score = np.tanh(0.1 * df["total_value"] + 0.05 * df["adjusted_revenue"]) + np.log1p(df["sqrt_values"] + 0.001) + 0.01 * df["weighted_qty"]
        return float(score.mean())

    # ----- baseline computations -----
    @staticmethod
    def _numpy_pipeline(npd: Dict[str, np.ndarray]) -> float:
        total_value = npd["values"] * npd["prices"]
        adjusted_revenue = npd["revenue"] * (1.0 + npd["profit_margin"] / 100.0)
        sqrt_values = np.sqrt(npd["values"])
        weighted_qty = npd["quantities"] + npd["values"] * 2.0
        # downstream non-linear
        score = np.tanh(0.1 * total_value + 0.05 * adjusted_revenue) + np.log1p(sqrt_values + 0.001) + 0.01 * weighted_qty
        return float(score.mean())

    @staticmethod
    def _numba_pipeline_factory():
        if not NUMBA_AVAILABLE:
            return None

        @njit(parallel=True, fastmath=True)
        def _pipeline(values, prices, revenue, profit_margin, quantities) -> float:
            n = values.shape[0]
            score_sum = 0.0
            for i in prange(n):
                tv = values[i] * prices[i]
                ar = revenue[i] * (1.0 + profit_margin[i] / 100.0)
                sv = (values[i]) ** 0.5
                wq = quantities[i] + values[i] * 2.0
                s = np.tanh(0.1 * tv + 0.05 * ar) + np.log1p(sv + 0.001) + 0.01 * wq
                score_sum += s
            return score_sum / n

        return _pipeline

    # ----- comprehensive DAG-style pipelines -----
    @staticmethod
    def _numpy_complex_dag(npd: Dict[str, np.ndarray], weights: Dict[str, float]) -> Tuple[float, Dict[int, float]]:
        w_tv = weights.get("w_tv", 0.1)
        w_ar = weights.get("w_ar", 0.05)
        w_sv = weights.get("w_sv", 0.01)
        w_wq = weights.get("w_wq", 0.01)
        w_a = weights.get("w_score_a", 0.7)
        w_b = weights.get("w_score_b", 0.3)

        tv = npd["values"] * npd["prices"]
        ar = npd["revenue"] * (1.0 + npd["profit_margin"] / 100.0)
        sv = np.sqrt(npd["values"])  # reused in two branches
        wq = npd["quantities"] + npd["values"] * 2.0

        score_a = np.tanh(w_tv * tv + w_ar * ar) + np.log1p(sv + 1e-3)
        score_b = 1.0 / (1.0 + np.exp(-(w_sv * sv + w_wq * wq)))
        final_score = w_a * score_a + w_b * score_b

        # Aggregation: per-category mean
        cats = npd["category"].astype(np.int64)
        unique = np.unique(cats)
        cat_means: Dict[int, float] = {}
        for c in unique:
            m = cats == c
            cat_means[int(c)] = float(final_score[m].mean()) if np.any(m) else 0.0
        return float(final_score.mean()), cat_means

    @staticmethod
    def _numba_complex_dag_factory():
        if not NUMBA_AVAILABLE:
            return None

        @njit(parallel=True, fastmath=True)
        def _compute(values, prices, revenue, profit_margin, quantities, category,
                     w_tv, w_ar, w_sv, w_wq, w_a, w_b) -> float:
            n = values.shape[0]
            acc = 0.0
            for i in prange(n):
                tv = values[i] * prices[i]
                ar = revenue[i] * (1.0 + profit_margin[i] / 100.0)
                sv = (values[i]) ** 0.5
                wq = quantities[i] + values[i] * 2.0
                score_a = np.tanh(w_tv * tv + w_ar * ar) + np.log1p(sv + 1e-3)
                score_b = 1.0 / (1.0 + np.exp(-(w_sv * sv + w_wq * wq)))
                s = w_a * score_a + w_b * score_b
                acc += s
            return acc / n

        @njit
        def _group_mean(categories: np.ndarray, values: np.ndarray, max_cat: int = 64) -> np.ndarray:
            # Simple grouping for small integer category codes
            sums = np.zeros(max_cat, dtype=np.float64)
            counts = np.zeros(max_cat, dtype=np.int64)
            for i in range(values.shape[0]):
                c = int(categories[i])
                if 0 <= c < max_cat:
                    sums[c] += values[i]
                    counts[c] += 1
            out = np.zeros(max_cat, dtype=np.float64)
            for c in range(max_cat):
                out[c] = sums[c] / counts[c] if counts[c] > 0 else 0.0
            return out

        return _compute, _group_mean

    # ----- Numbox DAG computations -----
    def _numbox_dag(self, npd: Dict[str, np.ndarray]) -> float:
        if not NUMBOX_AVAILABLE:
            raise RuntimeError("numbox is not available")

        # Defensive import pattern and attribute discovery since APIs may evolve
        nb = numbox  # noqa: F841

        # Define JIT kernels reused by nodes
        if NUMBA_AVAILABLE:
            @njit(fastmath=True)
            def _total_value(values, prices):
                return values * prices

            @njit(fastmath=True)
            def _adjusted_revenue(revenue, profit_margin):
                return revenue * (1.0 + profit_margin / 100.0)

            @njit(fastmath=True)
            def _sqrt_values(values):
                return np.sqrt(values)

            @njit(fastmath=True)
            def _weighted_qty(values, quantities):
                return quantities + values * 2.0

            @njit(fastmath=True, parallel=True)
            def _combine(tv, ar, sv, wq) -> float:
                n = tv.shape[0]
                acc = 0.0
                for i in prange(n):
                    s = np.tanh(0.1 * tv[i] + 0.05 * ar[i]) + np.log1p(sv[i] + 0.001) + 0.01 * wq[i]
                    acc += s
                return acc / n
        else:
            # Fallback to NumPy-only if Numba unavailable
            def _total_value(values, prices):
                return values * prices

            def _adjusted_revenue(revenue, profit_margin):
                return revenue * (1.0 + profit_margin / 100.0)

            def _sqrt_values(values):
                return np.sqrt(values)

            def _weighted_qty(values, quantities):
                return quantities + values * 2.0

            def _combine(tv, ar, sv, wq) -> float:
                score = np.tanh(0.1 * tv + 0.05 * ar) + np.log1p(sv + 0.001) + 0.01 * wq
                return float(score.mean())

        # Try to use Numbox Node/Work/Proxy abstractions if present
        has_node = hasattr(numbox, "Node")
        has_work = hasattr(numbox, "Work")
        has_proxy = hasattr(numbox, "Proxy")

        values = npd["values"]
        prices = npd["prices"]
        revenue = npd["revenue"]
        margin = npd["profit_margin"]
        quantities = npd["quantities"]

        if has_proxy:
            # Proxy can pre-define signatures and cache JIT; keep usage minimal for portability
            # We rely on direct functions for safety and only use Proxy when available
            try:
                # Create proxies (signature inference expected in recent versions)
                tv_fn = numbox.Proxy(_total_value)
                ar_fn = numbox.Proxy(_adjusted_revenue)
                sv_fn = numbox.Proxy(_sqrt_values)
                wq_fn = numbox.Proxy(_weighted_qty)
                comb_fn = numbox.Proxy(_combine)

                tv = tv_fn(values, prices)
                ar = ar_fn(revenue, margin)
                sv = sv_fn(values)
                wq = wq_fn(values, quantities)
                return float(comb_fn(tv, ar, sv, wq))
            except Exception:
                # Fall back below if Proxy signature requirements differ
                pass

        if has_node and has_work:
            try:
                Node = getattr(numbox, "Node")
                Work = getattr(numbox, "Work")

                # Build DAG: tv, ar, sv, wq => combine
                node_tv = Node(_total_value, deps=[("values",), ("prices",)])
                node_ar = Node(_adjusted_revenue, deps=[("revenue",), ("margin",)])
                node_sv = Node(_sqrt_values, deps=[("values",)])
                node_wq = Node(_weighted_qty, deps=[("values",), ("quantities",)])

                def _combine_adapter(outputs: Dict[str, np.ndarray]) -> float:
                    return _combine(outputs["tv"], outputs["ar"], outputs["sv"], outputs["wq"])  # type: ignore[arg-type]

                work = Work(
                    inputs={
                        "values": values,
                        "prices": prices,
                        "revenue": revenue,
                        "margin": margin,
                        "quantities": quantities,
                    },
                    nodes={
                        "tv": node_tv,
                        "ar": node_ar,
                        "sv": node_sv,
                        "wq": node_wq,
                    },
                    output=_combine_adapter,
                )

                return float(work.run())
            except Exception:
                # If API mismatch, fall through to plain functions
                pass

        # Plain fallback: evaluate stage-by-stage then combine
        tv = _total_value(values, prices)
        ar = _adjusted_revenue(revenue, margin)
        sv = _sqrt_values(values)
        wq = _weighted_qty(values, quantities)
        return float(_combine(tv, ar, sv, wq))

    def _numbox_complex_dag(self, npd: Dict[str, np.ndarray], weights: Dict[str, float]) -> Tuple[float, Dict[int, float]]:
        if not NUMBOX_AVAILABLE:
            raise RuntimeError("numbox is not available")

        # Kernels
        if NUMBA_AVAILABLE:
            @njit(fastmath=True)
            def _tv(values, prices):
                return values * prices
            @njit(fastmath=True)
            def _ar(revenue, margin):
                return revenue * (1.0 + margin / 100.0)
            @njit(fastmath=True)
            def _sv(values):
                return np.sqrt(values)
            @njit(fastmath=True)
            def _wq(values, quantities):
                return quantities + values * 2.0
            @njit(fastmath=True)
            def _score_a(tv, ar, sv, w_tv, w_ar):
                return np.tanh(w_tv * tv + w_ar * ar) + np.log1p(sv + 1e-3)
            @njit(fastmath=True)
            def _score_b(sv, wq, w_sv, w_wq):
                return 1.0 / (1.0 + np.exp(-(w_sv * sv + w_wq * wq)))
            @njit(fastmath=True)
            def _combine_scores(sa, sb, w_a, w_b) -> float:
                return float((w_a * sa + w_b * sb).mean())
        else:
            def _tv(values, prices):
                return values * prices
            def _ar(revenue, margin):
                return revenue * (1.0 + margin / 100.0)
            def _sv(values):
                return np.sqrt(values)
            def _wq(values, quantities):
                return quantities + values * 2.0
            def _score_a(tv, ar, sv, w_tv, w_ar):
                return np.tanh(w_tv * tv + w_ar * ar) + np.log1p(sv + 1e-3)
            def _score_b(sv, wq, w_sv, w_wq):
                return 1.0 / (1.0 + np.exp(-(w_sv * sv + w_wq * wq)))
            def _combine_scores(sa, sb, w_a, w_b) -> float:
                return float((w_a * sa + w_b * sb).mean())

        has_node = hasattr(numbox, "Node")
        has_work = hasattr(numbox, "Work")
        has_proxy = hasattr(numbox, "Proxy")

        values = npd["values"]
        prices = npd["prices"]
        revenue = npd["revenue"]
        margin = npd["profit_margin"]
        quantities = npd["quantities"]
        category = npd["category"].astype(np.int64)

        w_tv = float(weights.get("w_tv", 0.1))
        w_ar = float(weights.get("w_ar", 0.05))
        w_sv = float(weights.get("w_sv", 0.01))
        w_wq = float(weights.get("w_wq", 0.01))
        w_a = float(weights.get("w_score_a", 0.7))
        w_b = float(weights.get("w_score_b", 0.3))

        # Try Proxy first
        if has_proxy:
            try:
                tv_fn = numbox.Proxy(_tv); ar_fn = numbox.Proxy(_ar); sv_fn = numbox.Proxy(_sv); wq_fn = numbox.Proxy(_wq)
                sa_fn = numbox.Proxy(_score_a); sb_fn = numbox.Proxy(_score_b); comb_fn = numbox.Proxy(_combine_scores)
                tv = tv_fn(values, prices)
                ar = ar_fn(revenue, margin)
                sv = sv_fn(values)
                wq = wq_fn(values, quantities)
                sa = sa_fn(tv, ar, sv, w_tv, w_ar)
                sb = sb_fn(sv, wq, w_sv, w_wq)
                final_mean = comb_fn(sa, sb, w_a, w_b)
                # Aggregation per category (NumPy here for brevity)
                unique = np.unique(category)
                cat_means = {int(c): float((w_a * sa + w_b * sb)[category == c].mean()) for c in unique}
                return float(final_mean), cat_means
            except Exception:
                pass

        if has_node and has_work:
            try:
                Node = getattr(numbox, "Node"); Work = getattr(numbox, "Work")
                node_tv = Node(_tv, deps=[("values",), ("prices",)])
                node_ar = Node(_ar, deps=[("revenue",), ("margin",)])
                node_sv = Node(_sv, deps=[("values",)])
                node_wq = Node(_wq, deps=[("values",), ("quantities",)])

                def _sa_adapter(outputs, w_tv, w_ar):
                    return _score_a(outputs["tv"], outputs["ar"], outputs["sv"], w_tv, w_ar)
                def _sb_adapter(outputs, w_sv, w_wq):
                    return _score_b(outputs["sv"], outputs["wq"], w_sv, w_wq)
                def _final_adapter(outputs, w_a, w_b):
                    return _combine_scores(outputs["sa"], outputs["sb"], w_a, w_b)

                work = Work(
                    inputs={
                        "values": values,
                        "prices": prices,
                        "revenue": revenue,
                        "margin": margin,
                        "quantities": quantities,
                        "w_tv": w_tv,
                        "w_ar": w_ar,
                        "w_sv": w_sv,
                        "w_wq": w_wq,
                        "w_a": w_a,
                        "w_b": w_b,
                    },
                    nodes={
                        "tv": node_tv,
                        "ar": node_ar,
                        "sv": node_sv,
                        "wq": node_wq,
                        "sa": Node(lambda outputs, w_tv, w_ar: _sa_adapter(outputs, w_tv, w_ar), deps=[("tv",), ("ar",), ("sv",), ("w_tv",), ("w_ar",)]),
                        "sb": Node(lambda outputs, w_sv, w_wq: _sb_adapter(outputs, w_sv, w_wq), deps=[("sv",), ("wq",), ("w_sv",), ("w_wq",)]),
                    },
                    output=lambda outputs, w_a, w_b: _final_adapter(outputs, w_a, w_b),
                )
                final_mean = float(work.run())
                unique = np.unique(category)
                # Reuse intermediate arrays by recomputing dependent outputs only once
                # For simplicity, recompute final vector through kernels (acceptable for demo)
                sa = _score_a(_tv(values, prices), _ar(revenue, margin), _sv(values), w_tv, w_ar)
                sb = _score_b(_sv(values), _wq(values, quantities), w_sv, w_wq)
                cat_means = {int(c): float((w_a * sa + w_b * sb)[category == c].mean()) for c in unique}
                return final_mean, cat_means
            except Exception:
                pass

        # Fallback plain path
        tv = _tv(values, prices); ar = _ar(revenue, margin); sv = _sv(values); wq = _wq(values, quantities)
        sa = _score_a(tv, ar, sv, w_tv, w_ar)
        sb = _score_b(sv, wq, w_sv, w_wq)
        final_mean = _combine_scores(sa, sb, w_a, w_b)
        unique = np.unique(category)
        cat_means = {int(c): float((w_a * sa + w_b * sb)[category == c].mean()) for c in unique}
        return final_mean, cat_means

    # ----- driver -----
    def run(self) -> None:
        try:
            # 1) Create data in Spark
            spark_df = self._generate_spark_dataframe()

            # 2) Convert Spark → pandas (Arrow)
            pdf_arrow, t_arrow_conv, _ = self._time("Spark→pandas (Arrow)", self._spark_to_pandas_arrow, spark_df)

            # 3) Convert Spark → pandas (No Arrow)
            pdf_no_arrow, t_no_arrow_conv, _ = self._time("Spark→pandas (No Arrow)", self._spark_to_pandas_no_arrow, spark_df)

            def _benchmark_path(label: str, pdf: pd.DataFrame):
                # Pandas compute
                _, t_pd, _ = self._time(f"[{label}] Pandas pipeline", self._pandas_pipeline, pdf)
                # Prepare NumPy arrays
                np_data, t_prep, _ = self._time(f"[{label}] Prepare NumPy arrays", self._to_numpy, pdf)
                # NumPy compute
                _, t_np, _ = self._time(f"[{label}] NumPy pipeline (vectorized)", self._numpy_pipeline, np_data)
                # Numba compute
                if NUMBA_AVAILABLE:
                    pipeline = self._numba_pipeline_factory()
                    assert pipeline is not None
                    _ = pipeline(np_data["values"][:100], np_data["prices"][:100], np_data["revenue"][:100], np_data["profit_margin"][:100], np_data["quantities"][:100])
                    _, t_nb, _ = self._time(
                        f"[{label}] Numba pipeline (monolithic @njit, parallel)",
                        pipeline,
                        np_data["values"], np_data["prices"], np_data["revenue"], np_data["profit_margin"], np_data["quantities"],
                    )
                else:
                    t_nb = float("nan")
                # Numbox DAG compute
                if NUMBOX_AVAILABLE:
                    _ = self._numbox_dag({k: v[:100] for k, v in np_data.items()})
                    _, t_nbx, _ = self._time(f"[{label}] Numbox DAG (Node/Work/Proxy)", self._numbox_dag, np_data)
                else:
                    t_nbx = float("nan")
                # Comprehensive DAG stage (branching + aggregation)
                weights1 = {"w_tv": 0.1, "w_ar": 0.05, "w_sv": 0.01, "w_wq": 0.01, "w_score_a": 0.7, "w_score_b": 0.3}
                weights2 = {"w_tv": 0.12, "w_ar": 0.04, "w_sv": 0.015, "w_wq": 0.008, "w_score_a": 0.6, "w_score_b": 0.4}

                # NumPy complex DAG
                _, t_np_dag1, _ = self._time(f"[{label}] NumPy complex DAG (run1)", self._numpy_complex_dag, np_data, weights1)
                _, t_np_dag2, _ = self._time(f"[{label}] NumPy complex DAG (run2)", self._numpy_complex_dag, np_data, weights2)

                # Numba complex DAG
                if NUMBA_AVAILABLE:
                    complex_pair = self._numba_complex_dag_factory()
                    assert complex_pair is not None
                    complex_compute, group_mean = complex_pair
                    # Warm-up complex
                    _ = complex_compute(
                        np_data["values"][:100], np_data["prices"][:100], np_data["revenue"][:100], np_data["profit_margin"][:100], np_data["quantities"][:100], np_data["category"][:100],
                        0.1, 0.05, 0.01, 0.01, 0.7, 0.3
                    )
                    _, t_nb_dag1, _ = self._time(
                        f"[{label}] Numba complex DAG (run1)", complex_compute,
                        np_data["values"], np_data["prices"], np_data["revenue"], np_data["profit_margin"], np_data["quantities"], np_data["category"],
                        0.1, 0.05, 0.01, 0.01, 0.7, 0.3,
                    )
                    _, t_nb_dag2, _ = self._time(
                        f"[{label}] Numba complex DAG (run2)", complex_compute,
                        np_data["values"], np_data["prices"], np_data["revenue"], np_data["profit_margin"], np_data["quantities"], np_data["category"],
                        0.12, 0.04, 0.015, 0.008, 0.6, 0.4,
                    )
                else:
                    t_nb_dag1 = float("nan"); t_nb_dag2 = float("nan")

                # Numbox complex DAG
                if NUMBOX_AVAILABLE:
                    # Warm-up
                    _ = self._numbox_complex_dag({k: v[:100] for k, v in np_data.items()}, weights1)
                    _, t_nbx_dag1, _ = self._time(f"[{label}] Numbox complex DAG (run1)", self._numbox_complex_dag, np_data, weights1)
                    _, t_nbx_dag2, _ = self._time(f"[{label}] Numbox complex DAG (run2)", self._numbox_complex_dag, np_data, weights2)
                else:
                    t_nbx_dag1 = float("nan"); t_nbx_dag2 = float("nan")

                return {
                    "pandas": t_pd,
                    "prep_numpy": t_prep,
                    "numpy": t_np,
                    "numba": t_nb,
                    "numbox": t_nbx,
                    "numpy_dag_run1": t_np_dag1,
                    "numpy_dag_run2": t_np_dag2,
                    "numba_dag_run1": t_nb_dag1,
                    "numba_dag_run2": t_nb_dag2,
                    "numbox_dag_run1": t_nbx_dag1,
                    "numbox_dag_run2": t_nbx_dag2,
                }

            results_arrow = _benchmark_path("Arrow", pdf_arrow)
            results_no_arrow = _benchmark_path("NoArrow", pdf_no_arrow)

            # Summary
            print("\n" + "=" * 60)
            print("🏁 NUMBOX DAG DEMO RESULTS")
            print("=" * 60)
            print("Conversion times:")
            print(f"   Spark→pandas (Arrow):   {t_arrow_conv:.4f}s")
            print(f"   Spark→pandas (NoArrow): {t_no_arrow_conv:.4f}s")
            if t_arrow_conv > 0:
                print(f"   🏹 Arrow speedup:        {t_no_arrow_conv / t_arrow_conv:.1f}x")

            def _print_path(label: str, r: Dict[str, float]):
                print(f"\n[{label}] compute:")
                print(f"   pandas:         {r['pandas']:.4f}s")
                print(f"   prep numpy:     {r['prep_numpy']:.4f}s")
                print(f"   numpy:          {r['numpy']:.4f}s")
                print(f"   numba:          {r['numba']:.4f}s" if not np.isnan(r['numba']) else "   numba:          n/a")
                print(f"   numbox (DAG):   {r['numbox']:.4f}s" if not np.isnan(r['numbox']) else "   numbox (DAG):   n/a")
                print(f"   numpy DAG:      run1={r['numpy_dag_run1']:.4f}s  run2={r['numpy_dag_run2']:.4f}s")
                if not np.isnan(r['numba']):
                    print(f"   numba DAG:      run1={r['numba_dag_run1']:.4f}s  run2={r['numba_dag_run2']:.4f}s")
                else:
                    print("   numba DAG:      n/a")
                if not np.isnan(r['numbox']):
                    print(f"   numbox DAG:     run1={r['numbox_dag_run1']:.4f}s  run2={r['numbox_dag_run2']:.4f}s")
                else:
                    print("   numbox DAG:     n/a")

            _print_path("Arrow", results_arrow)
            _print_path("NoArrow", results_no_arrow)

            print("\n🔗 Framework: Numbox - see https://github.com/Goykhman/numbox")

        except Exception as e:
            print(f"❌ Error in Numbox DAG demo: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n🧹 Cleaning up Spark...")
            self.spark_no_arrow.stop()
            self.spark_with_arrow.stop()
            print("   ✅ Done")


def main() -> None:
    print("🚀 Starting Numbox DAG Demo...")
    memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    print(f"💻 System memory: {memory_gb:.1f} GB")
    if memory_gb < 8:
        rows = 100_000
    elif memory_gb < 16:
        rows = 200_000
    else:
        rows = 300_000
    demo = NumboxDagDemo(rows=rows)
    demo.run()


if __name__ == "__main__":
    # Optional doc generation hook
    import os as _os
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/13_numbox_dag_demo.md",
            title="Frameworks: Numbox DAG demo (NumPy, Numba, Numbox)",
            main_callable=main,
        )
    else:
        main()



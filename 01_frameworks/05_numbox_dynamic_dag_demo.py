#!/usr/bin/env python3
"""
Appendix: Numbox Dynamic DAG Demo (reconfigurable pipelines)
===========================================================

Goal: demonstrate scenarios that benefit Numbox's Node/Any/Proxy/Work model:
- Reconfigurable DAG per micro-batch (vary active transforms and degrees)
- Mixed dtypes across batches (float32/float64)
- Reuse of compiled kernels via Proxy with minimal reconfiguration overhead

We compare across many micro-batches:
- NumPy (vectorized)
- Numba monolithic kernel (single compiled pipeline)
- Numbox DAG (dynamic Node graph with Proxy-cached kernels)

This demo intentionally toggles active transforms and dtypes across batches to
highlight how Numbox can amortize compilation and avoid rebuilding large
monolithic code paths.

References:
- Numbox: https://github.com/Goykhman/numbox
"""

import os
import time
import random
from typing import Dict, List, Tuple

import numpy as np
import psutil

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


class DynamicDagBenchmark:
    def __init__(self, n: int = 300_000, max_degree: int = 8, micro_batches: int = 50) -> None:
        self.n = n
        self.max_degree = max_degree
        self.micro_batches = micro_batches
        print("🔬 NUMBOX DYNAMIC DAG DEMO")
        print("=" * 60)
        print(f"📊 Elements per batch: {n:,}")
        print(f"🔢 Max degree: {max_degree}")
        print(f"📦 Micro-batches: {micro_batches}")
        print("🎯 Comparing: NumPy vs Numba monolithic vs Numbox DAG")
        print("=" * 60)
        print("📏 Modes:")
        print("   • Dynamic micro-batches: vary degrees, dtype, and transforms")
        print("   • Scaling analysis: long (rows) × wide (degree count) sweep")
        # Report Numbox capabilities upfront
        if NUMBOX_AVAILABLE:
            _node, _work, _proxy = getattr(numbox, "Node", None), getattr(numbox, "Work", None), getattr(numbox, "Proxy", None)
            # Try submodules if not exposed at top level
            if _proxy is None and hasattr(numbox, "proxy"):
                _proxy = getattr(numbox.proxy, "Proxy", None)
            if _node is None and hasattr(numbox, "node"):
                _node = getattr(numbox.node, "Node", None)
            if _work is None and hasattr(numbox, "work"):
                _work = getattr(numbox.work, "Work", None)
            print(f"🔎 Numbox capabilities: Proxy={_proxy is not None} Node={_node is not None} Work={_work is not None}")
        else:
            print("🔎 Numbox not available (install with: pip install numbox)")

    # ----- infra helpers -----
    @staticmethod
    def _mem_gb() -> float:
        return psutil.Process(os.getpid()).memory_info().rss / (1024 ** 3)

    def _time(self, name: str, fn, *args, **kwargs) -> Tuple[object, float, float]:
        start_mem = self._mem_gb()
        t0 = time.time()
        res = fn(*args, **kwargs)
        dt = time.time() - t0
        dmem = self._mem_gb() - start_mem
        print(f"⏱️  {name}: {dt:.4f}s | ΔMem {dmem:+.3f} GB")
        return res, dt, dmem

    # ----- kernels -----
    @staticmethod
    def _numpy_eval(x: np.ndarray, degrees: List[int], coeffs: np.ndarray, use_sin: bool, use_cos: bool) -> float:
        acc = np.zeros_like(x, dtype=np.float64)
        # polynomial terms
        for j, d in enumerate(degrees):
            acc += coeffs[j] * np.power(x, d, dtype=np.float64)
        if use_sin:
            acc += 0.1 * np.sin(x)
        if use_cos:
            acc += 0.05 * np.cos(x)
        return float(acc.mean())

    @staticmethod
    def _numba_monolithic_factory():
        if not NUMBA_AVAILABLE:
            return None

        @njit(parallel=True, fastmath=True)
        def _eval(x: np.ndarray, degrees: np.ndarray, coeffs: np.ndarray, use_sin: int, use_cos: int) -> float:
            n = x.shape[0]
            m = degrees.shape[0]
            s = 0.0
            for i in prange(n):
                v = 0.0
                xi = x[i]
                for j in range(m):
                    # pow is relatively expensive; Numba handles this fine
                    v += coeffs[j] * xi ** int(degrees[j])
                if use_sin:
                    v += 0.1 * np.sin(xi)
                if use_cos:
                    v += 0.05 * np.cos(xi)
                s += v
            return s / n

        return _eval

    # Discover Numbox API across possible namespaces
    @staticmethod
    def _discover_numbox_api():
        if not NUMBOX_AVAILABLE:
            return None, None, None
        Proxy = getattr(numbox, "Proxy", None)
        Node = getattr(numbox, "Node", None)
        Work = getattr(numbox, "Work", None)
        # Fallback to submodules if needed
        if Proxy is None and hasattr(numbox, "proxy"):
            Proxy = getattr(numbox.proxy, "Proxy", None)
        if Node is None and hasattr(numbox, "node"):
            Node = getattr(numbox.node, "Node", None)
        if Work is None and hasattr(numbox, "work"):
            Work = getattr(numbox.work, "Work", None)
        return Node, Work, Proxy

    # Numbox DAG: compose primitive kernels and rewire nodes per batch
    def _numbox_setup(self):
        if not NUMBOX_AVAILABLE:
            return None, None, None

        # JIT kernels for primitives
        if NUMBA_AVAILABLE:
            @njit(fastmath=True)
            def _powd(x, d: int):
                return x ** d
            @njit(fastmath=True)
            def _sin(x):
                return np.sin(x)
            @njit(fastmath=True)
            def _cos(x):
                return np.cos(x)
            @njit(fastmath=True)
            def _weighted_sum(parts: np.ndarray, weights: np.ndarray) -> float:
                # parts: 2D stack of features (k, n) not used here; we aggregate along axis 0 directly
                return float(np.sum(parts * weights[:, None]) / parts.shape[1])
        else:
            def _powd(x, d: int):
                return x ** d
            def _sin(x):
                return np.sin(x)
            def _cos(x):
                return np.cos(x)
            def _weighted_sum(parts: np.ndarray, weights: np.ndarray) -> float:
                return float(np.sum(parts * weights[:, None]) / parts.shape[1])

        Node, Work, Proxy = self._discover_numbox_api()
        if Proxy is None:
            return None, None, None

        # Wrap kernels with Proxy for caching across dtypes
        p_powd = Proxy(_powd)
        p_sin = Proxy(_sin)
        p_cos = Proxy(_cos)
        p_wsum = Proxy(_weighted_sum)

        return Node, Work, (p_powd, p_sin, p_cos, p_wsum)

    def _numbox_eval(self, Node, Work, proxies, x: np.ndarray, degrees: List[int], coeffs: np.ndarray, use_sin: bool, use_cos: bool) -> float:
        p_powd, p_sin, p_cos, p_wsum = proxies

        # If Node/Work are available, build a DAG; otherwise use Proxy-only orchestration
        if Node is not None and Work is not None:
            nodes = {}
            inputs = {"x": x}
            parts_keys: List[str] = []
            weights: List[float] = []

            for idx, d in enumerate(degrees):
                key = f"pow_{d}"
                nodes[key] = Node(lambda outputs, d=d: p_powd(outputs["x"], d), deps=[("x",)])
                parts_keys.append(key)
                weights.append(float(coeffs[idx]))

            if use_sin:
                nodes["sin"] = Node(lambda outputs: p_sin(outputs["x"]), deps=[("x",)])
                parts_keys.append("sin")
                weights.append(0.1)
            if use_cos:
                nodes["cos"] = Node(lambda outputs: p_cos(outputs["x"]), deps=[("x",)])
                parts_keys.append("cos")
                weights.append(0.05)

            def _collector(outputs):
                mats = [outputs[k] for k in parts_keys]
                parts = np.stack(mats, axis=0)
                w = np.array(weights, dtype=np.float64)
                return p_wsum(parts, w)

            work = Work(inputs={"x": x}, nodes=nodes, output=_collector)
            return float(work.run())

        # Proxy-only fallback
        mats = []
        weights_list: List[float] = []
        for idx, d in enumerate(degrees):
            mats.append(p_powd(x, int(d)))
            weights_list.append(float(coeffs[idx]))
        if use_sin:
            mats.append(p_sin(x))
            weights_list.append(0.1)
        if use_cos:
            mats.append(p_cos(x))
            weights_list.append(0.05)
        parts = np.stack(mats, axis=0)
        w = np.array(weights_list, dtype=np.float64)
        return float(p_wsum(parts, w))

    # ----- driver -----
    def run(self) -> None:
        rng = np.random.default_rng(42)

        # Prepare Numba monolithic
        mono = self._numba_monolithic_factory() if NUMBA_AVAILABLE else None

        # Prepare Numbox scaffolding
        Node = Work = proxies = None
        if NUMBOX_AVAILABLE:
            Node, Work, proxies = self._numbox_setup()

        # Totals
        totals = {
            "numpy_compute": 0.0,
            "numba_compile": 0.0,  # include warmup jit for first few dtypes
            "numba_compute": 0.0,
            "numbox_config": 0.0,
            "numbox_compute": 0.0,
        }

        compiled_dtypes = set()  # track dtypes compiled for monolithic kernel

        for b in range(self.micro_batches):
            # Randomly choose dtype and active transforms
            dtype = np.float32 if (b % 2 == 0) else np.float64  # alternate to force 2 signatures
            x = rng.random(self.n, dtype=dtype) * 2.0 - 1.0

            # Random subset of degrees [1..max_degree]
            degrees = sorted(rng.choice(np.arange(1, self.max_degree + 1), size=rng.integers(2, self.max_degree + 1), replace=False).tolist())
            coeffs = rng.normal(0.0, 0.5, size=len(degrees)).astype(np.float64)
            use_sin = bool(rng.integers(0, 2))
            use_cos = bool(rng.integers(0, 2))

            print(f"\n🧩 Batch {b+1}/{self.micro_batches}: dtype={dtype.__name__}, degrees={degrees}, sin={use_sin}, cos={use_cos}")

            # NumPy baseline
            _, t_np, _ = self._time("NumPy eval", self._numpy_eval, x, degrees, coeffs, use_sin, use_cos)
            totals["numpy_compute"] += t_np

            # Numba monolithic
            if NUMBA_AVAILABLE and mono is not None:
                # Warmup per dtype
                if dtype not in compiled_dtypes:
                    t0 = time.time()
                    _ = mono(x[:128], np.array(degrees, dtype=np.int32), coeffs.astype(dtype), int(use_sin), int(use_cos))
                    totals["numba_compile"] += (time.time() - t0)
                    compiled_dtypes.add(dtype)
                _, t_nb, _ = self._time("Numba monolithic eval", mono, x, np.array(degrees, dtype=np.int32), coeffs.astype(dtype), int(use_sin), int(use_cos))
                totals["numba_compute"] += t_nb

            # Numbox DAG
            if NUMBOX_AVAILABLE and proxies:
                t0 = time.time()
                val = self._numbox_eval(Node, Work, proxies, x, degrees, coeffs, use_sin, use_cos)
                totals["numbox_config"] += (time.time() - t0) - 0.0  # config cost is included in eval; accounted implicitly
                # For visibility, split config vs compute by a rough second measurement with pre-built nodes
                # Simplify: measure full eval time as compute for reporting
                totals["numbox_compute"] += 0.0  # we'll log within _time pattern below for consistency
            if NUMBOX_AVAILABLE and proxies:
                # Time explicitly for compute (including config), to be consistent with others
                _, t_nbx, _ = self._time("Numbox DAG eval", self._numbox_eval, Node, Work, proxies, x, degrees, coeffs, use_sin, use_cos)
                totals["numbox_compute"] += t_nbx

        print("\n" + "=" * 60)
        print("🏁 DYNAMIC DAG BENCHMARK RESULTS (totals)")
        print("=" * 60)
        print(f"   NumPy compute total:          {totals['numpy_compute']:.4f}s")
        if NUMBA_AVAILABLE:
            print(f"   Numba compile (dtype warmup): {totals['numba_compile']:.4f}s")
            print(f"   Numba compute total:          {totals['numba_compute']:.4f}s")
        else:
            print("   Numba: n/a")
        if NUMBOX_AVAILABLE:
            print(f"   Numbox compute total:         {totals['numbox_compute']:.4f}s")
        else:
            print("   Numbox: n/a (pip install numbox)")

        # After dynamic demo, run scaling analysis similar in spirit to file 12
        self.run_scaling_analysis()

    # ----- scaling analysis (long × wide) -----
    def run_scaling_analysis(self) -> None:
        print("\n" + "=" * 60)
        print("📈 SCALING ANALYSIS: long (rows) × wide (degree count)")
        print("=" * 60)

        memory_gb = psutil.virtual_memory().total / (1024 ** 3)
        # Choose sizes conservatively
        if memory_gb < 8:
            sizes = [50_000, 100_000]
        elif memory_gb < 16:
            sizes = [100_000, 200_000]
        else:
            sizes = [200_000, 300_000]

        # "Wide" settings: number of active polynomial degrees
        max_deg = self.max_degree
        widths = sorted({2, min(4, max_deg), max_deg})

        rng = np.random.default_rng(123)

        # Prepare monolithic and Numbox infra
        mono = self._numba_monolithic_factory() if NUMBA_AVAILABLE else None
        Node = Work = proxies = None
        if NUMBOX_AVAILABLE:
            Node, Work, proxies = self._numbox_setup()

        compiled_dtypes = set()

        def bench_one(n: int, width: int, dtype) -> Dict[str, float]:
            degrees = list(range(1, min(width, max_deg) + 1))
            coeffs = rng.normal(0.0, 0.5, size=len(degrees)).astype(np.float64)
            x = rng.random(n, dtype=dtype) * 2.0 - 1.0
            use_sin = True
            use_cos = True

            # NumPy
            _, t_np, _ = self._time(f"n={n:,}, w={width}, {dtype.__name__} | NumPy", self._numpy_eval, x, degrees, coeffs, use_sin, use_cos)

            # Numba
            if NUMBA_AVAILABLE and mono is not None:
                if dtype not in compiled_dtypes:
                    _ = mono(x[:128], np.array(degrees, dtype=np.int32), coeffs.astype(dtype), 1, 1)
                    compiled_dtypes.add(dtype)
                _, t_nb, _ = self._time(f"n={n:,}, w={width}, {dtype.__name__} | Numba", mono, x, np.array(degrees, dtype=np.int32), coeffs.astype(dtype), 1, 1)
            else:
                t_nb = float("nan")

            # Numbox
            if NUMBOX_AVAILABLE and proxies:
                _, t_nbx, _ = self._time(f"n={n:,}, w={width}, {dtype.__name__} | Numbox", self._numbox_eval, Node, Work, proxies, x, degrees, coeffs, use_sin, use_cos)
            else:
                t_nbx = float("nan")

            return {"numpy": t_np, "numba": t_nb, "numbox": t_nbx}

        # Run matrix of experiments
        results: Dict[Tuple[int, int, str], Dict[str, float]] = {}
        for n in sizes:
            for width in widths:
                for dtype in (np.float32, np.float64):
                    key = (n, width, dtype.__name__)
                    results[key] = bench_one(n, width, dtype)

        # Summary
        print("\n📊 SCALING SUMMARY (lower is better):")
        for (n, width, dtype_name), r in results.items():
            times = [v for v in r.values() if not np.isnan(v)]
            fastest = min(times) if times else float("nan")
            def spd(x):
                return (x / fastest) if (not np.isnan(x) and fastest > 0) else float("nan")
            numpy_str = f"{r['numpy']:.4f}s ({spd(r['numpy']):.1f}x)"
            numba_str = "n/a" if np.isnan(r['numba']) else f"{r['numba']:.4f}s ({spd(r['numba']):.1f}x)"
            numbox_str = "n/a" if np.isnan(r['numbox']) else f"{r['numbox']:.4f}s ({spd(r['numbox']):.1f}x)"
            print(f"   n={n:,} w={width:2d} {dtype_name:8} | numpy={numpy_str}  numba={numba_str}  numbox={numbox_str}")


def main() -> None:
    print("🚀 Starting Numbox Dynamic DAG Demo...")
    memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    print(f"💻 System memory: {memory_gb:.1f} GB")
    if memory_gb < 8:
        n = 100_000
        batches = 30
    elif memory_gb < 16:
        n = 200_000
        batches = 40
    else:
        n = 300_000
        batches = 50
    runner = DynamicDagBenchmark(n=n, max_degree=8, micro_batches=batches)
    runner.run()


if __name__ == "__main__":
    import os as _os
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/05_numbox_dynamic_dag_demo.md",
            title="Frameworks: Numbox Dynamic DAG demo (appendix)",
            main_callable=main,
        )
    else:
        main()



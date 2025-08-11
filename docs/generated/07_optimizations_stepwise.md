# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:30 UTC

## Console output

```text
🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==
   convert: 0.684s | transform: 0.188s | forecast: 0.205s | total: 1.077s

== Step 1: Projection (convert all wide columns vs slim) ==
   convert: 2.275s | transform: 0.006s | forecast: 0.043s | total: 2.324s
   Δ vs baseline (slim): +1.247s

== Step 2: Dtype tuning (float32 compute) ==
   convert: 0.141s | transform: 0.007s | forecast: 0.051s | total: 0.198s
   Δ vs baseline (f64): -0.879s

== Step 3: JIT warmup (second run) ==
   convert: 0.142s | transform: 0.006s | forecast: 0.051s | total: 0.198s
   convert: 0.128s | transform: 0.006s | forecast: 0.052s | total: 0.186s
   first: 0.198s | second: 0.186s | Δ: -0.012s

== Step 4: Threads control (OMP/MKL) ==
   convert: 0.127s | transform: 0.006s | forecast: 0.049s | total: 0.182s
   convert: 0.138s | transform: 0.006s | forecast: 0.046s | total: 0.190s
   1-thread: 0.182s | 4-threads: 0.190s | Δ: +0.008s

🏁 Summary (lower is better):
   Baseline (naive):   1.077s
   Step 1 (full width): 2.324s
   Step 2 (float32):    0.198s
   Step 3 (warm 2nd):   0.186s
   Step 4 (thr ctrl):   0.182s
```

# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:43 UTC

## Console output

```text
🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==
   convert: 0.611s | transform: 0.184s | forecast: 0.204s | total: 0.999s

ℹ️  Projection is assumed: converting only needed columns (avoid full width).

== Step 2: Dtype tuning (float32 compute on Arrow→pandas path) ==
   convert: 0.170s | transform: 0.005s | forecast: 0.049s | total: 0.224s
   Δ vs baseline (float64): -0.775s

== Step 3: Repartition by entity + mapInPandas (fused kernel) ==
   Δ vs baseline: +1.040s

== Step 4: Approximate sigmoid (tanh-based) in fused kernel ==
   Δ vs step3: -1.402s

🏁 Summary (lower is better):
   Baseline (slim):     0.999s
   Step 2 (float32):    0.224s
   Step 3 (stream):     2.039s
   Step 4 (approx σ):   0.637s
```

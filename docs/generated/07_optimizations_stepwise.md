# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:38 UTC

## Console output

```text
🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==
   convert: 0.739s | transform: 0.188s | forecast: 0.201s | total: 1.128s

ℹ️  Projection is assumed: converting only needed columns (avoid full width).

== Step 2: Repartition by entity + mapInPandas (fused kernel) ==
   Δ vs baseline: +0.936s

== Step 3: Approximate sigmoid (tanh-based) in fused kernel ==
   Δ vs step2: -1.411s

🏁 Summary (lower is better):
   Baseline (slim):     1.128s
   Step 2 (stream):     2.064s
   Step 3 (approx σ):   0.653s
```

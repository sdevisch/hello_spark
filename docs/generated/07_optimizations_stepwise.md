# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:33 UTC

## Console output

```text
🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==
   convert: 0.664s | transform: 0.200s | forecast: 0.286s | total: 1.150s

== Step 1: Projection (convert all wide columns vs slim) ==
   convert: 2.276s | transform: 0.005s | forecast: 0.041s | total: 2.322s
   Δ vs baseline (slim): +1.172s

== Step 2: Repartition by entity + mapInPandas (fused kernel) ==
   Δ vs baseline: +0.920s

== Step 3: Approximate sigmoid (tanh-based) in fused kernel ==
   Δ vs step2: -1.416s

🏁 Summary (lower is better):
   Baseline (naive):   1.150s
   Step 1 (full width): 2.322s
   Step 2 (stream):     2.070s
   Step 3 (approx σ):   0.654s
```

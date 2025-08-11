# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:45 UTC

## Console output

```text
🚀 Stepwise optimization experiment (built on 06 baseline: Arrow→pandas→NumPy/Numba)
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline (06): Arrow→pandas→NumPy/Numba (slim cols, float64) ==
   convert: 0.695s | transform: 0.192s | forecast: 0.204s | total: 1.090s

ℹ️  Projection is assumed: converting only needed columns (avoid full width).

== Step 2: Dtype tuning (float32 compute on Arrow→pandas path) ==
   convert: 0.185s | transform: 0.005s | forecast: 0.044s | total: 0.233s
   Δ vs baseline (float64): -0.857s

== Step 3: Repartition by entity + mapInPandas (fused kernel) ==
   Δ vs baseline: +0.935s

== Step 4: Approximate sigmoid (tanh-based) in fused kernel ==
   Δ vs step3: -1.376s

🏁 Summary (lower is better):
   Baseline (slim):     1.090s
   Step 2 (float32):    0.233s
   Step 3 (stream):     2.025s
   Step 4 (approx σ):   0.649s

📌 Guidance on streaming (mapInPandas):
   • Streaming keeps work distributed and avoids collecting to the driver.
   • In small local runs, overhead (repartition, Arrow batches, per-partition pandas frames, per-executor JIT warmup)
     can outweigh compute, so it may appear slower in this benchmark.
   • Enable it when: per-entity series are long, horizon is large, driver memory is tight, or end-to-end distribution is required.
   • If used, cache the repartitioned data, warm JIT once per executor, right-size partitions (≈2–3× cores), and limit OMP/MKL threads.
```

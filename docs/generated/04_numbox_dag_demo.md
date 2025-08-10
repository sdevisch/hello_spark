# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-10 22:53 UTC

## Scope

Appendix: niche DAG structuring (Numbox) for specialized scenarios.

## Console output

```text
🚀 Starting Numbox DAG Demo...
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
🔬 NUMBOX DAG DEMO
============================================================
📊 Dataset size: 300,000 rows
🎯 Comparing: Pandas vs NumPy vs Numba vs Numbox (DAG)
============================================================
🌐 Spark UI (No Arrow): http://localhost:4040
🌐 Spark UI (With Arrow): http://localhost:4041
⏱️  Create Spark DataFrame (cached)
   ✅ 0.9499s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4814s | ΔMem +0.051 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 5.7447s | ΔMem +0.076 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0104s | ΔMem +0.027 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0043s | ΔMem +0.000 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2372s | ΔMem +0.011 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0107s | ΔMem +0.016 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0107s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2860s | ΔMem +0.006 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2564s | ΔMem +0.001 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0088s | ΔMem +0.013 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0037s | ΔMem +0.009 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2786s | ΔMem +0.002 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0113s | ΔMem +0.011 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0115s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2895s | ΔMem +0.001 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2533s | ΔMem +0.001 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4814s
   Spark→pandas (NoArrow): 5.7447s
   🏹 Arrow speedup:        11.9x

[Arrow] compute:
   pandas:         0.0104s
   prep numpy:     0.0001s
   numpy:          0.0043s
   numba:          0.0004s
   numbox (DAG):   0.2372s
   numpy DAG:      run1=0.0107s  run2=0.0107s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2860s  run2=0.2564s

[NoArrow] compute:
   pandas:         0.0088s
   prep numpy:     0.0001s
   numpy:          0.0037s
   numba:          0.0004s
   numbox (DAG):   0.2786s
   numpy DAG:      run1=0.0113s  run2=0.0115s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2895s  run2=0.2533s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

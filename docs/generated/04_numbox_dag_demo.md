# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-10 16:54 UTC

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
   ✅ 0.9476s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4452s | ΔMem +0.051 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 6.0170s | ΔMem +0.079 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0112s | ΔMem +0.031 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0045s | ΔMem +0.009 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2467s | ΔMem +0.003 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0114s | ΔMem +0.003 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0111s | ΔMem +0.020 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2578s | ΔMem +0.003 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2916s | ΔMem +0.002 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0086s | ΔMem +0.011 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0046s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2434s | ΔMem +0.001 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0109s | ΔMem +0.011 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0108s | ΔMem +0.002 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2539s | ΔMem +0.001 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2558s | ΔMem +0.003 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4452s
   Spark→pandas (NoArrow): 6.0170s
   🏹 Arrow speedup:        13.5x

[Arrow] compute:
   pandas:         0.0112s
   prep numpy:     0.0001s
   numpy:          0.0045s
   numba:          0.0004s
   numbox (DAG):   0.2467s
   numpy DAG:      run1=0.0114s  run2=0.0111s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2578s  run2=0.2916s

[NoArrow] compute:
   pandas:         0.0086s
   prep numpy:     0.0001s
   numpy:          0.0046s
   numba:          0.0004s
   numbox (DAG):   0.2434s
   numpy DAG:      run1=0.0109s  run2=0.0108s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2539s  run2=0.2558s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

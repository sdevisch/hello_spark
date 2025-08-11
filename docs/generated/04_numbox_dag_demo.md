# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-11 01:58 UTC

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
   ✅ 0.9275s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4079s | ΔMem +0.050 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 5.6998s | ΔMem +0.189 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0103s | ΔMem +0.000 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0045s | ΔMem +0.000 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2362s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0111s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0103s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2483s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2844s | ΔMem +0.000 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0079s | ΔMem +0.000 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0036s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2728s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0110s | ΔMem +0.005 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0105s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2530s | ΔMem +0.002 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2863s | ΔMem +0.003 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4079s
   Spark→pandas (NoArrow): 5.6998s
   🏹 Arrow speedup:        14.0x

[Arrow] compute:
   pandas:         0.0103s
   prep numpy:     0.0001s
   numpy:          0.0045s
   numba:          0.0004s
   numbox (DAG):   0.2362s
   numpy DAG:      run1=0.0111s  run2=0.0103s
   numba DAG:      run1=0.0006s  run2=0.0006s
   numbox DAG:     run1=0.2483s  run2=0.2844s

[NoArrow] compute:
   pandas:         0.0079s
   prep numpy:     0.0001s
   numpy:          0.0036s
   numba:          0.0004s
   numbox (DAG):   0.2728s
   numpy DAG:      run1=0.0110s  run2=0.0105s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2530s  run2=0.2863s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

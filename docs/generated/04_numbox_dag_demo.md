# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-10 16:24 UTC

## Console output

```text
🚀 Starting Numbox DAG Demo...
💻 System memory: 18.0 GB
🔬 NUMBOX DAG DEMO
============================================================
📊 Dataset size: 300,000 rows
🎯 Comparing: Pandas vs NumPy vs Numba vs Numbox (DAG)
============================================================
🌐 Spark UI (No Arrow): http://localhost:4040
🌐 Spark UI (With Arrow): http://localhost:4041
⏱️  Create Spark DataFrame (cached)
   ✅ 0.9465s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4387s | ΔMem +0.051 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 5.9907s | ΔMem +0.079 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0101s | ΔMem +0.027 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0048s | ΔMem +0.009 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2408s | ΔMem +0.005 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0111s | ΔMem +0.012 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0112s | ΔMem +0.011 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2542s | ΔMem +0.010 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2916s | ΔMem +0.007 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0086s | ΔMem +0.000 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0039s | ΔMem +0.007 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2446s | ΔMem +0.001 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0107s | ΔMem +0.005 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0103s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2534s | ΔMem +0.002 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2552s | ΔMem +0.004 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4387s
   Spark→pandas (NoArrow): 5.9907s
   🏹 Arrow speedup:        13.7x

[Arrow] compute:
   pandas:         0.0101s
   prep numpy:     0.0001s
   numpy:          0.0048s
   numba:          0.0004s
   numbox (DAG):   0.2408s
   numpy DAG:      run1=0.0111s  run2=0.0112s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2542s  run2=0.2916s

[NoArrow] compute:
   pandas:         0.0086s
   prep numpy:     0.0001s
   numpy:          0.0039s
   numba:          0.0004s
   numbox (DAG):   0.2446s
   numpy DAG:      run1=0.0107s  run2=0.0103s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2534s  run2=0.2552s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-10 16:18 UTC

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
   ✅ 0.9381s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4863s | ΔMem +0.051 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 5.7470s | ΔMem +0.075 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0087s | ΔMem +0.029 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0038s | ΔMem +0.009 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2401s | ΔMem +0.003 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0110s | ΔMem +0.007 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0108s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2532s | ΔMem +0.008 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2868s | ΔMem +0.002 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0083s | ΔMem +0.005 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0039s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2456s | ΔMem +0.001 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0110s | ΔMem +0.013 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0106s | ΔMem +0.013 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2542s | ΔMem +0.002 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2950s | ΔMem +0.003 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4863s
   Spark→pandas (NoArrow): 5.7470s
   🏹 Arrow speedup:        11.8x

[Arrow] compute:
   pandas:         0.0087s
   prep numpy:     0.0001s
   numpy:          0.0038s
   numba:          0.0004s
   numbox (DAG):   0.2401s
   numpy DAG:      run1=0.0110s  run2=0.0108s
   numba DAG:      run1=0.0005s  run2=0.0005s
   numbox DAG:     run1=0.2532s  run2=0.2868s

[NoArrow] compute:
   pandas:         0.0083s
   prep numpy:     0.0001s
   numpy:          0.0039s
   numba:          0.0004s
   numbox (DAG):   0.2456s
   numpy DAG:      run1=0.0110s  run2=0.0106s
   numba DAG:      run1=0.0005s  run2=0.0005s
   numbox DAG:     run1=0.2542s  run2=0.2950s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

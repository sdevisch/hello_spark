# Frameworks: Numbox DAG demo (NumPy, Numba, Numbox)

Generated: 2025-08-10 15:13 UTC

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
   ✅ 0.9314s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4138s | ΔMem +0.051 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 5.8070s | ΔMem +0.078 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0093s | ΔMem +0.027 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0042s | ΔMem +0.007 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2481s | ΔMem +0.006 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0109s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0112s | ΔMem +0.007 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2548s | ΔMem +0.010 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.3582s | ΔMem +0.006 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0083s | ΔMem +0.016 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0037s | ΔMem +0.007 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0004s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2513s | ΔMem +0.001 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0108s | ΔMem +0.011 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0101s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2509s | ΔMem +0.002 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2549s | ΔMem +0.003 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4138s
   Spark→pandas (NoArrow): 5.8070s
   🏹 Arrow speedup:        14.0x

[Arrow] compute:
   pandas:         0.0093s
   prep numpy:     0.0001s
   numpy:          0.0042s
   numba:          0.0004s
   numbox (DAG):   0.2481s
   numpy DAG:      run1=0.0109s  run2=0.0112s
   numba DAG:      run1=0.0006s  run2=0.0005s
   numbox DAG:     run1=0.2548s  run2=0.3582s

[NoArrow] compute:
   pandas:         0.0083s
   prep numpy:     0.0001s
   numpy:          0.0037s
   numba:          0.0004s
   numbox (DAG):   0.2513s
   numpy DAG:      run1=0.0108s  run2=0.0101s
   numba DAG:      run1=0.0005s  run2=0.0005s
   numbox DAG:     run1=0.2509s  run2=0.2549s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

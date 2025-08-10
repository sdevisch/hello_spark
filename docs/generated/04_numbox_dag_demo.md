# Frameworks: Numbox DAG demo (appendix)

Generated: 2025-08-10 17:01 UTC

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
   ✅ 0.9207s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark→pandas (Arrow)
   ✅ 0.4307s | ΔMem +0.052 GB
⏱️  Spark→pandas (No Arrow)
   ✅ 6.0236s | ΔMem +0.071 GB
⏱️  [Arrow] Pandas pipeline
   ✅ 0.0106s | ΔMem +0.027 GB
⏱️  [Arrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [Arrow] NumPy pipeline (vectorized)
   ✅ 0.0047s | ΔMem +0.012 GB
⏱️  [Arrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2406s | ΔMem +0.003 GB
⏱️  [Arrow] NumPy complex DAG (run1)
   ✅ 0.0108s | ΔMem +0.009 GB
⏱️  [Arrow] NumPy complex DAG (run2)
   ✅ 0.0110s | ΔMem +0.007 GB
⏱️  [Arrow] Numba complex DAG (run1)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numba complex DAG (run2)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [Arrow] Numbox complex DAG (run1)
   ✅ 0.2518s | ΔMem +0.004 GB
⏱️  [Arrow] Numbox complex DAG (run2)
   ✅ 0.2882s | ΔMem +0.002 GB
⏱️  [NoArrow] Pandas pipeline
   ✅ 0.0084s | ΔMem +0.013 GB
⏱️  [NoArrow] Prepare NumPy arrays
   ✅ 0.0001s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy pipeline (vectorized)
   ✅ 0.0040s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba pipeline (monolithic @njit, parallel)
   ✅ 0.0005s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox DAG (Node/Work/Proxy)
   ✅ 0.2405s | ΔMem +0.002 GB
⏱️  [NoArrow] NumPy complex DAG (run1)
   ✅ 0.0112s | ΔMem +0.000 GB
⏱️  [NoArrow] NumPy complex DAG (run2)
   ✅ 0.0108s | ΔMem +0.011 GB
⏱️  [NoArrow] Numba complex DAG (run1)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numba complex DAG (run2)
   ✅ 0.0006s | ΔMem +0.000 GB
⏱️  [NoArrow] Numbox complex DAG (run1)
   ✅ 0.2503s | ΔMem +0.002 GB
⏱️  [NoArrow] Numbox complex DAG (run2)
   ✅ 0.2536s | ΔMem +0.003 GB

============================================================
🏁 NUMBOX DAG DEMO RESULTS
============================================================
Conversion times:
   Spark→pandas (Arrow):   0.4307s
   Spark→pandas (NoArrow): 6.0236s
   🏹 Arrow speedup:        14.0x

[Arrow] compute:
   pandas:         0.0106s
   prep numpy:     0.0001s
   numpy:          0.0047s
   numba:          0.0005s
   numbox (DAG):   0.2406s
   numpy DAG:      run1=0.0108s  run2=0.0110s
   numba DAG:      run1=0.0005s  run2=0.0005s
   numbox DAG:     run1=0.2518s  run2=0.2882s

[NoArrow] compute:
   pandas:         0.0084s
   prep numpy:     0.0001s
   numpy:          0.0040s
   numba:          0.0005s
   numbox (DAG):   0.2405s
   numpy DAG:      run1=0.0112s  run2=0.0108s
   numba DAG:      run1=0.0006s  run2=0.0006s
   numbox DAG:     run1=0.2503s  run2=0.2536s

🔗 Framework: Numbox - see https://github.com/Goykhman/numbox

🧹 Cleaning up Spark...
   ✅ Done
```

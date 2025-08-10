# Frameworks: Panel xbeta & cashflows (appendix case)

Generated: 2025-08-10 16:24 UTC

## Console output

```text
🚀 Starting Xbeta & Cashflows Panel Comparison...
💻 System memory: 18.0 GB
🔬 XBETAs & CASHFLOWS COMPARISON (panel data)
============================================================
📊 Target rows (approx): 300,000
🎯 Data starts in Spark; we compare frameworks on xbeta & rolling sums
============================================================
🌐 Spark UI: http://localhost:4040 (or 4041)

============================================================
📊 CREATING PANEL DATA IN SPARK (entities × days)
============================================================
   Entities: 1,500 | Days: 200 | Target rows≈300,000
⏱️  Build Spark panel (with betas, features, xbeta, CF, rolling)
   ✅ 1.1432s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2703s | ΔMem -0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.5283s | ΔMem +0.194 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.1809s | ΔMem +0.144 GB
   🏹 Arrow speedup Spark→pandas: 21.2x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0610s | ΔMem +0.088 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0144s | ΔMem +0.013 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0178s | ΔMem +0.031 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0045s | ΔMem +0.000 GB
⏱️  Numba: rolling 30d cash_flow per entity
   ✅ 0.0005s | ΔMem +0.000 GB

============================================================
🏁 RESULTS (wall times)
============================================================
🔎 Terminology:
   • Conversion: Spark→pandas with/without Arrow
   • Prep: pandas→NumPy array preparation (sorting, view extraction)
   • Compute only: pure algorithm time (no conversion/prep)
   • Total: conversion + prep + compute

📦 Conversion timings:
   Spark→pandas (Arrow):   0.5283s
   Spark→pandas (NoArrow): 11.1809s
   🏹 Arrow speedup:        21.2x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0144s
   From pandas (NoArrow):  0.0178s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0045s
   Numba (rolling 30d):    0.0005s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.5472s
   NumPy total (NoArrow):  11.2032s
   Numba total (Arrow):    0.5477s
   Numba total (NoArrow):  11.2036s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2703s
   Pandas (rolling):       0.0610s

🧹 Cleaning up Spark...
   ✅ Done
```

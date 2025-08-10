# Frameworks: Panel xbeta & cashflows (appendix case)

Generated: 2025-08-10 16:18 UTC

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
   ✅ 1.1453s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2783s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.5677s | ΔMem +0.193 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.0898s | ΔMem +0.149 GB
   🏹 Arrow speedup Spark→pandas: 19.5x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0640s | ΔMem +0.095 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0139s | ΔMem +0.011 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0190s | ΔMem +0.034 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0042s | ΔMem +0.000 GB
⏱️  Numba: rolling 30d cash_flow per entity
   ✅ 0.0006s | ΔMem +0.000 GB

============================================================
🏁 RESULTS (wall times)
============================================================
🔎 Terminology:
   • Conversion: Spark→pandas with/without Arrow
   • Prep: pandas→NumPy array preparation (sorting, view extraction)
   • Compute only: pure algorithm time (no conversion/prep)
   • Total: conversion + prep + compute

📦 Conversion timings:
   Spark→pandas (Arrow):   0.5677s
   Spark→pandas (NoArrow): 11.0898s
   🏹 Arrow speedup:        19.5x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0139s
   From pandas (NoArrow):  0.0190s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0042s
   Numba (rolling 30d):    0.0006s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.5857s
   NumPy total (NoArrow):  11.1130s
   Numba total (Arrow):    0.5863s
   Numba total (NoArrow):  11.1136s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2783s
   Pandas (rolling):       0.0640s

🧹 Cleaning up Spark...
   ✅ Done
```

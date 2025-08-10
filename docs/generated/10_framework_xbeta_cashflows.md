# Frameworks: Panel xbeta & cashflows comparison

Generated: 2025-08-10 15:13 UTC

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
   ✅ 1.1075s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2408s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.9067s | ΔMem +0.192 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.4706s | ΔMem +0.140 GB
   🏹 Arrow speedup Spark→pandas: 12.7x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0654s | ΔMem +0.087 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0135s | ΔMem +0.011 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0181s | ΔMem +0.021 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0036s | ΔMem +0.000 GB
⏱️  Numba: rolling 30d cash_flow per entity
   ✅ 0.0004s | ΔMem +0.000 GB

============================================================
🏁 RESULTS (wall times)
============================================================
🔎 Terminology:
   • Conversion: Spark→pandas with/without Arrow
   • Prep: pandas→NumPy array preparation (sorting, view extraction)
   • Compute only: pure algorithm time (no conversion/prep)
   • Total: conversion + prep + compute

📦 Conversion timings:
   Spark→pandas (Arrow):   0.9067s
   Spark→pandas (NoArrow): 11.4706s
   🏹 Arrow speedup:        12.7x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0135s
   From pandas (NoArrow):  0.0181s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0036s
   Numba (rolling 30d):    0.0004s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.9238s
   NumPy total (NoArrow):  11.4922s
   Numba total (Arrow):    0.9242s
   Numba total (NoArrow):  11.4926s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2408s
   Pandas (rolling):       0.0654s

🧹 Cleaning up Spark...
   ✅ Done
```

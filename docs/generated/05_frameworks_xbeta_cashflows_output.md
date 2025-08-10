# Frameworks: Panel xbeta & cashflows comparison

Generated: 2025-08-10 13:58 UTC

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
   ✅ 1.1300s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2857s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.5415s | ΔMem +0.188 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 15.2292s | ΔMem +0.131 GB
   🏹 Arrow speedup Spark→pandas: 28.1x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0547s | ΔMem +0.089 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0135s | ΔMem +0.011 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0148s | ΔMem +0.022 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0028s | ΔMem +0.000 GB
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
   Spark→pandas (Arrow):   0.5415s
   Spark→pandas (NoArrow): 15.2292s
   🏹 Arrow speedup:        28.1x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0135s
   From pandas (NoArrow):  0.0148s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0028s
   Numba (rolling 30d):    0.0006s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.5579s
   NumPy total (NoArrow):  15.2468s
   Numba total (Arrow):    0.5585s
   Numba total (NoArrow):  15.2474s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2857s
   Pandas (rolling):       0.0547s

🧹 Cleaning up Spark...
   ✅ Done
```

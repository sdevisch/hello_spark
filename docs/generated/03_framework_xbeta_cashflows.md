# Frameworks: Panel xbeta & cashflows (appendix case)

Generated: 2025-08-10 16:31 UTC

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
   ✅ 1.1601s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2735s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.4710s | ΔMem +0.194 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.3832s | ΔMem +0.146 GB
   🏹 Arrow speedup Spark→pandas: 24.2x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0607s | ΔMem +0.079 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0162s | ΔMem +0.023 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0189s | ΔMem +0.033 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0038s | ΔMem +0.002 GB
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
   Spark→pandas (Arrow):   0.4710s
   Spark→pandas (NoArrow): 11.3832s
   🏹 Arrow speedup:        24.2x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0162s
   From pandas (NoArrow):  0.0189s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0038s
   Numba (rolling 30d):    0.0005s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.4910s
   NumPy total (NoArrow):  11.4059s
   Numba total (Arrow):    0.4915s
   Numba total (NoArrow):  11.4065s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2735s
   Pandas (rolling):       0.0607s

🧹 Cleaning up Spark...
   ✅ Done
```

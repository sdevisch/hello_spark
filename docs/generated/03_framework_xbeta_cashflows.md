# Frameworks: Panel xbeta & cashflows (appendix case)

Generated: 2025-08-10 17:01 UTC

## Scope

Case study supporting the frameworks conclusion (panel xbeta & cashflows).

## Console output

```text
🚀 Starting Xbeta & Cashflows Panel Comparison...
📚 Docs index: docs/index.md
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
   ✅ 1.1479s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2433s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.5460s | ΔMem +0.194 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.1561s | ΔMem +0.149 GB
   🏹 Arrow speedup Spark→pandas: 20.4x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0582s | ΔMem +0.093 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0149s | ΔMem +0.015 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0175s | ΔMem +0.028 GB
⏱️  NumPy: xbeta + cash_flow (vectorized)
   ✅ 0.0031s | ΔMem +0.000 GB
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
   Spark→pandas (Arrow):   0.5460s
   Spark→pandas (NoArrow): 11.1561s
   🏹 Arrow speedup:        20.4x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0149s
   From pandas (NoArrow):  0.0175s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0031s
   Numba (rolling 30d):    0.0005s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.5639s
   NumPy total (NoArrow):  11.1767s
   Numba total (Arrow):    0.5644s
   Numba total (NoArrow):  11.1771s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2433s
   Pandas (rolling):       0.0582s

🧹 Cleaning up Spark...
   ✅ Done
```

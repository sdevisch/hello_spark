# Frameworks: Panel xbeta & cashflows (appendix case)

Generated: 2025-08-10 22:54 UTC

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
   ✅ 1.1387s | ΔMem +0.000 GB
   ✅ Materialized rows: 300,000
⏱️  Spark compute (reuse xbeta, CF rolling, entity agg)
   ✅ 0.2808s | ΔMem +0.000 GB
⏱️  Convert Spark→pandas (Arrow)
   ✅ 0.5581s | ΔMem +0.192 GB
⏱️  Convert Spark→pandas (No Arrow)
   ✅ 11.2419s | ΔMem +0.315 GB
   🏹 Arrow speedup Spark→pandas: 20.1x
⏱️  Pandas compute (rolling per entity)
   ✅ 0.0571s | ΔMem +0.000 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (Arrow)
   ✅ 0.0131s | ΔMem +0.000 GB
⏱️  Prepare NumPy arrays (sorted by entity/day) from pandas (NoArrow)
   ✅ 0.0156s | ΔMem +0.000 GB
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
   Spark→pandas (Arrow):   0.5581s
   Spark→pandas (NoArrow): 11.2419s
   🏹 Arrow speedup:        20.1x

🧰 Prep timings (pandas→NumPy):
   From pandas (Arrow):    0.0131s
   From pandas (NoArrow):  0.0156s

⚙️  Compute-only timings:
   NumPy (xbeta + cf):     0.0031s
   Numba (rolling 30d):    0.0005s

📈 End-to-end totals (conversion + prep + compute):
   NumPy total (Arrow):    0.5742s
   NumPy total (NoArrow):  11.2606s
   Numba total (Arrow):    0.5747s
   Numba total (NoArrow):  11.2611s

🖥️  In-framework compute-only:
   Spark (reuse/agg):      0.2808s
   Pandas (rolling):       0.0571s

🧹 Cleaning up Spark...
   ✅ Done
```

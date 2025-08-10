# Frameworks: Numbox Dynamic DAG demo (appendix)

Generated: 2025-08-10 17:01 UTC

## Scope

Appendix: niche DAG structuring (Numbox) for specialized scenarios.

## Console output

```text
🚀 Starting Numbox Dynamic DAG Demo...
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
🔬 NUMBOX DYNAMIC DAG DEMO
============================================================
📊 Elements per batch: 300,000
🔢 Max degree: 8
📦 Micro-batches: 50
🎯 Comparing: NumPy vs Numba monolithic vs Numbox DAG
============================================================
📏 Modes:
   • Dynamic micro-batches: vary degrees, dtype, and transforms
   • Scaling analysis: long (rows) × wide (degree count) sweep
🔎 Numbox capabilities: Proxy=False Node=False Work=False

🧩 Batch 1/50: dtype=float32, degrees=[5, 6, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0145s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 2/50: dtype=float64, degrees=[1, 2, 3, 4, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0136s | ΔMem +0.009 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 3/50: dtype=float32, degrees=[1, 2, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0063s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 4/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0228s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 5/50: dtype=float32, degrees=[6, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0068s | ΔMem +0.004 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 6/50: dtype=float64, degrees=[1, 5, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0103s | ΔMem +0.005 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 7/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0225s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 8/50: dtype=float64, degrees=[1, 4, 5, 7], sin=True, cos=False
⏱️  NumPy eval: 0.0132s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 9/50: dtype=float32, degrees=[2, 3, 4, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0163s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 10/50: dtype=float64, degrees=[2, 3, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0188s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 11/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0235s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0012s | ΔMem +0.000 GB

🧩 Batch 12/50: dtype=float64, degrees=[1, 2, 6, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0093s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 13/50: dtype=float32, degrees=[2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0198s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 14/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0228s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 15/50: dtype=float32, degrees=[1, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0059s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 16/50: dtype=float64, degrees=[2, 4, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0070s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 17/50: dtype=float32, degrees=[1, 2, 3, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0191s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 18/50: dtype=float64, degrees=[1, 2], sin=True, cos=False
⏱️  NumPy eval: 0.0042s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 19/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7], sin=True, cos=False
⏱️  NumPy eval: 0.0197s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 20/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0212s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 21/50: dtype=float32, degrees=[1, 5, 6], sin=True, cos=True
⏱️  NumPy eval: 0.0104s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 22/50: dtype=float64, degrees=[3, 5, 6, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0141s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 23/50: dtype=float32, degrees=[3, 4, 6], sin=True, cos=True
⏱️  NumPy eval: 0.0112s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 24/50: dtype=float64, degrees=[1, 2], sin=False, cos=True
⏱️  NumPy eval: 0.0042s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 25/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0221s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 26/50: dtype=float64, degrees=[1, 5, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0100s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 27/50: dtype=float32, degrees=[1, 5], sin=False, cos=False
⏱️  NumPy eval: 0.0059s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 28/50: dtype=float64, degrees=[1, 2, 3], sin=True, cos=True
⏱️  NumPy eval: 0.0084s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 29/50: dtype=float32, degrees=[3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0191s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 30/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0237s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 31/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0226s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 32/50: dtype=float64, degrees=[3, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0152s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 33/50: dtype=float32, degrees=[3, 4, 5, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0129s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 34/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0237s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 35/50: dtype=float32, degrees=[1, 4, 5, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0165s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 36/50: dtype=float64, degrees=[1, 3, 4, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0161s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 37/50: dtype=float32, degrees=[1, 2, 3, 5, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0133s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 38/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0193s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 39/50: dtype=float32, degrees=[3, 6], sin=False, cos=False
⏱️  NumPy eval: 0.0064s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 40/50: dtype=float64, degrees=[2, 3, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0161s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 41/50: dtype=float32, degrees=[1, 4, 6], sin=True, cos=False
⏱️  NumPy eval: 0.0096s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 42/50: dtype=float64, degrees=[3, 5, 6], sin=True, cos=False
⏱️  NumPy eval: 0.0109s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 43/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0226s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 44/50: dtype=float64, degrees=[1, 2, 3, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0195s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 45/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0231s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 46/50: dtype=float64, degrees=[4, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0077s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 47/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0230s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 48/50: dtype=float64, degrees=[2, 3, 5, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0141s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 49/50: dtype=float32, degrees=[4, 7], sin=True, cos=True
⏱️  NumPy eval: 0.0076s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 50/50: dtype=float64, degrees=[2, 3, 4, 5, 6, 7], sin=True, cos=True
⏱️  NumPy eval: 0.0186s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

============================================================
🏁 DYNAMIC DAG BENCHMARK RESULTS (totals)
============================================================
   NumPy compute total:          0.7454s
   Numba compile (dtype warmup): 0.5856s
   Numba compute total:          0.0397s
   Numbox compute total:         0.0000s

============================================================
📈 SCALING ANALYSIS: long (rows) × wide (degree count)
============================================================
⏱️  n=200,000, w=2, float32 | NumPy: 0.0028s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float32 | Numba: 0.0004s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float64 | NumPy: 0.0037s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float64 | Numba: 0.0004s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float32 | NumPy: 0.0073s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float32 | Numba: 0.0005s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float64 | NumPy: 0.0077s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float64 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float32 | NumPy: 0.0157s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float32 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float64 | NumPy: 0.0159s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float64 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float32 | NumPy: 0.0041s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float32 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float64 | NumPy: 0.0055s | ΔMem +0.002 GB
⏱️  n=300,000, w=2, float64 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float32 | NumPy: 0.0108s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float32 | Numba: 0.0007s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float64 | NumPy: 0.0115s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float64 | Numba: 0.0009s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float32 | NumPy: 0.0237s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float32 | Numba: 0.0011s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float64 | NumPy: 0.0241s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float64 | Numba: 0.0011s | ΔMem +0.000 GB

📊 SCALING SUMMARY (lower is better):
   n=200,000 w= 2 float32  | numpy=0.0028s (7.5x)  numba=0.0004s (1.0x)  numbox=n/a
   n=200,000 w= 2 float64  | numpy=0.0037s (8.9x)  numba=0.0004s (1.0x)  numbox=n/a
   n=200,000 w= 4 float32  | numpy=0.0073s (13.6x)  numba=0.0005s (1.0x)  numbox=n/a
   n=200,000 w= 4 float64  | numpy=0.0077s (12.9x)  numba=0.0006s (1.0x)  numbox=n/a
   n=200,000 w= 8 float32  | numpy=0.0157s (20.3x)  numba=0.0008s (1.0x)  numbox=n/a
   n=200,000 w= 8 float64  | numpy=0.0159s (19.7x)  numba=0.0008s (1.0x)  numbox=n/a
   n=300,000 w= 2 float32  | numpy=0.0041s (7.4x)  numba=0.0006s (1.0x)  numbox=n/a
   n=300,000 w= 2 float64  | numpy=0.0055s (9.2x)  numba=0.0006s (1.0x)  numbox=n/a
   n=300,000 w= 4 float32  | numpy=0.0108s (14.5x)  numba=0.0007s (1.0x)  numbox=n/a
   n=300,000 w= 4 float64  | numpy=0.0115s (12.5x)  numba=0.0009s (1.0x)  numbox=n/a
   n=300,000 w= 8 float32  | numpy=0.0237s (21.1x)  numba=0.0011s (1.0x)  numbox=n/a
   n=300,000 w= 8 float64  | numpy=0.0241s (21.4x)  numba=0.0011s (1.0x)  numbox=n/a
```

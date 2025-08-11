# Frameworks: Numbox Dynamic DAG demo (appendix)

Generated: 2025-08-11 01:58 UTC

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
⏱️  NumPy eval: 0.0144s | ΔMem +0.013 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 2/50: dtype=float64, degrees=[1, 2, 3, 4, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0134s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 3/50: dtype=float32, degrees=[1, 2, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0061s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 4/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0223s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 5/50: dtype=float32, degrees=[6, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0062s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 6/50: dtype=float64, degrees=[1, 5, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0098s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 7/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0224s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 8/50: dtype=float64, degrees=[1, 4, 5, 7], sin=True, cos=False
⏱️  NumPy eval: 0.0126s | ΔMem +0.007 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 9/50: dtype=float32, degrees=[2, 3, 4, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0165s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 10/50: dtype=float64, degrees=[2, 3, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0183s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 11/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0229s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0012s | ΔMem +0.000 GB

🧩 Batch 12/50: dtype=float64, degrees=[1, 2, 6, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0093s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 13/50: dtype=float32, degrees=[2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0191s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 14/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0222s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 15/50: dtype=float32, degrees=[1, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0057s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 16/50: dtype=float64, degrees=[2, 4, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0067s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 17/50: dtype=float32, degrees=[1, 2, 3, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0187s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 18/50: dtype=float64, degrees=[1, 2], sin=True, cos=False
⏱️  NumPy eval: 0.0040s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 19/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7], sin=True, cos=False
⏱️  NumPy eval: 0.0198s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 20/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0212s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 21/50: dtype=float32, degrees=[1, 5, 6], sin=True, cos=True
⏱️  NumPy eval: 0.0098s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 22/50: dtype=float64, degrees=[3, 5, 6, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0138s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 23/50: dtype=float32, degrees=[3, 4, 6], sin=True, cos=True
⏱️  NumPy eval: 0.0108s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 24/50: dtype=float64, degrees=[1, 2], sin=False, cos=True
⏱️  NumPy eval: 0.0041s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 25/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0219s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 26/50: dtype=float64, degrees=[1, 5, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0096s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 27/50: dtype=float32, degrees=[1, 5], sin=False, cos=False
⏱️  NumPy eval: 0.0056s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 28/50: dtype=float64, degrees=[1, 2, 3], sin=True, cos=True
⏱️  NumPy eval: 0.0082s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 29/50: dtype=float32, degrees=[3, 4, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0188s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 30/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0238s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 31/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0225s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0012s | ΔMem +0.000 GB

🧩 Batch 32/50: dtype=float64, degrees=[3, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0151s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 33/50: dtype=float32, degrees=[3, 4, 5, 7], sin=False, cos=False
⏱️  NumPy eval: 0.0126s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 34/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0235s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 35/50: dtype=float32, degrees=[1, 4, 5, 7, 8], sin=True, cos=True
⏱️  NumPy eval: 0.0162s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 36/50: dtype=float64, degrees=[1, 3, 4, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0167s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 37/50: dtype=float32, degrees=[1, 2, 3, 5, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0134s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0007s | ΔMem +0.000 GB

🧩 Batch 38/50: dtype=float64, degrees=[1, 2, 3, 4, 5, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0192s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0009s | ΔMem +0.000 GB

🧩 Batch 39/50: dtype=float32, degrees=[3, 6], sin=False, cos=False
⏱️  NumPy eval: 0.0066s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0004s | ΔMem +0.000 GB

🧩 Batch 40/50: dtype=float64, degrees=[2, 3, 5, 6, 7, 8], sin=False, cos=False
⏱️  NumPy eval: 0.0159s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 41/50: dtype=float32, degrees=[1, 4, 6], sin=True, cos=False
⏱️  NumPy eval: 0.0094s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 42/50: dtype=float64, degrees=[3, 5, 6], sin=True, cos=False
⏱️  NumPy eval: 0.0104s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 43/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0225s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 44/50: dtype=float64, degrees=[1, 2, 3, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0190s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

🧩 Batch 45/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0224s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0012s | ΔMem +0.000 GB

🧩 Batch 46/50: dtype=float64, degrees=[4, 7], sin=False, cos=True
⏱️  NumPy eval: 0.0076s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0005s | ΔMem +0.000 GB

🧩 Batch 47/50: dtype=float32, degrees=[1, 2, 3, 4, 5, 6, 7, 8], sin=True, cos=False
⏱️  NumPy eval: 0.0223s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0011s | ΔMem +0.000 GB

🧩 Batch 48/50: dtype=float64, degrees=[2, 3, 5, 7, 8], sin=False, cos=True
⏱️  NumPy eval: 0.0140s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0008s | ΔMem +0.000 GB

🧩 Batch 49/50: dtype=float32, degrees=[4, 7], sin=True, cos=True
⏱️  NumPy eval: 0.0079s | ΔMem +0.000 GB
⏱️  Numba monolithic eval: 0.0006s | ΔMem +0.000 GB

🧩 Batch 50/50: dtype=float64, degrees=[2, 3, 4, 5, 6, 7], sin=True, cos=True
⏱️  NumPy eval: 0.0182s | ΔMem +0.002 GB
⏱️  Numba monolithic eval: 0.0010s | ΔMem +0.000 GB

============================================================
🏁 DYNAMIC DAG BENCHMARK RESULTS (totals)
============================================================
   NumPy compute total:          0.7331s
   Numba compile (dtype warmup): 0.5879s
   Numba compute total:          0.0397s
   Numbox compute total:         0.0000s

============================================================
📈 SCALING ANALYSIS: long (rows) × wide (degree count)
============================================================
⏱️  n=200,000, w=2, float32 | NumPy: 0.0029s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float32 | Numba: 0.0004s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float64 | NumPy: 0.0040s | ΔMem +0.000 GB
⏱️  n=200,000, w=2, float64 | Numba: 0.0004s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float32 | NumPy: 0.0072s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float32 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float64 | NumPy: 0.0076s | ΔMem +0.000 GB
⏱️  n=200,000, w=4, float64 | Numba: 0.0005s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float32 | NumPy: 0.0154s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float32 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float64 | NumPy: 0.0156s | ΔMem +0.000 GB
⏱️  n=200,000, w=8, float64 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float32 | NumPy: 0.0046s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float32 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float64 | NumPy: 0.0054s | ΔMem +0.000 GB
⏱️  n=300,000, w=2, float64 | Numba: 0.0006s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float32 | NumPy: 0.0107s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float32 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=300,000, w=4, float64 | NumPy: 0.0116s | ΔMem +0.004 GB
⏱️  n=300,000, w=4, float64 | Numba: 0.0008s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float32 | NumPy: 0.0232s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float32 | Numba: 0.0013s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float64 | NumPy: 0.0240s | ΔMem +0.000 GB
⏱️  n=300,000, w=8, float64 | Numba: 0.0011s | ΔMem +0.000 GB

📊 SCALING SUMMARY (lower is better):
   n=200,000 w= 2 float32  | numpy=0.0029s (7.8x)  numba=0.0004s (1.0x)  numbox=n/a
   n=200,000 w= 2 float64  | numpy=0.0040s (10.0x)  numba=0.0004s (1.0x)  numbox=n/a
   n=200,000 w= 4 float32  | numpy=0.0072s (12.9x)  numba=0.0006s (1.0x)  numbox=n/a
   n=200,000 w= 4 float64  | numpy=0.0076s (14.2x)  numba=0.0005s (1.0x)  numbox=n/a
   n=200,000 w= 8 float32  | numpy=0.0154s (18.1x)  numba=0.0008s (1.0x)  numbox=n/a
   n=200,000 w= 8 float64  | numpy=0.0156s (19.7x)  numba=0.0008s (1.0x)  numbox=n/a
   n=300,000 w= 2 float32  | numpy=0.0046s (8.0x)  numba=0.0006s (1.0x)  numbox=n/a
   n=300,000 w= 2 float64  | numpy=0.0054s (9.4x)  numba=0.0006s (1.0x)  numbox=n/a
   n=300,000 w= 4 float32  | numpy=0.0107s (12.6x)  numba=0.0008s (1.0x)  numbox=n/a
   n=300,000 w= 4 float64  | numpy=0.0116s (15.1x)  numba=0.0008s (1.0x)  numbox=n/a
   n=300,000 w= 8 float32  | numpy=0.0232s (18.0x)  numba=0.0013s (1.0x)  numbox=n/a
   n=300,000 w= 8 float64  | numpy=0.0240s (21.6x)  numba=0.0011s (1.0x)  numbox=n/a
```

# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 01:21 UTC

## Console output

```text
🚀 Package vs pandas-on-Spark experiment
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB

================================================================================
🧪 Scenario: Small, in-memory compute-heavy (Numba sweet spot)
--------------------------------------------------------------------------------
rows=300,000, entities=500, horizon=48, wide_cols=0
~Estimated raw size (double-eqv): 0.01 GB
   Built panel rows: 300,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.517s; transform: 0.201s; forecast: 0.195s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.201s; forecast(spark, 48 steps): 1.125s

📊 Scenario summary:
   Package path total: 0.913s  (convert=0.517s, tf=0.201s, fc=0.195s, numba=True)
   pandas-on-Spark total: 1.326s (tf=0.201s, fc=1.125s)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Medium, some width (balanced)
--------------------------------------------------------------------------------
rows=600,000, entities=1,000, horizon=36, wide_cols=50
~Estimated raw size (double-eqv): 0.27 GB
   Built panel rows: 600,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.220s; transform: 0.001s; forecast: 0.050s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.220s; forecast(spark, 36 steps): 0.784s

📊 Scenario summary:
   Package path total: 0.271s  (convert=0.220s, tf=0.001s, fc=0.050s, numba=True)
   pandas-on-Spark total: 1.004s (tf=0.220s, fc=0.784s)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Wide (hundreds cols), moderate horizon
--------------------------------------------------------------------------------
rows=400,000, entities=1,000, horizon=24, wide_cols=200
~Estimated raw size (double-eqv): 0.66 GB
   Built panel rows: 400,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.467s; transform: 0.001s; forecast: 0.022s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.838s; forecast(spark, 24 steps): 2.362s

📊 Scenario summary:
   Package path total: 0.490s  (convert=0.467s, tf=0.001s, fc=0.022s, numba=True)
   pandas-on-Spark total: 3.200s (tf=0.838s, fc=2.362s)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Large rows (driver-safety block), horizon small
--------------------------------------------------------------------------------
rows=2,000,000, entities=2,000, horizon=12, wide_cols=50
~Estimated raw size (double-eqv): 0.90 GB
   Built panel rows: 2,000,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.343s; transform: 0.004s; forecast: 0.039s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.174s; forecast(spark, 12 steps): 0.415s

📊 Scenario summary:
   Package path total: 0.386s  (convert=0.343s, tf=0.004s, fc=0.039s, numba=True)
   pandas-on-Spark total: 0.588s (tf=0.174s, fc=0.415s)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.
```

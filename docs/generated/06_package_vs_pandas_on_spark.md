# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 02:25 UTC

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
   Convert (Arrow): 0.454s; transform: 0.174s; forecast: 0.194s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.201s; forecast(spark, 48 steps): 1.104s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 300,000, time: 1.720s, mean(y)=0.9988

📊 Scenario summary:
   Package path total: 0.822s  (convert=0.454s, tf=0.174s, fc=0.194s, numba=True)
   pandas-on-Spark total: 1.304s (tf=0.201s, fc=1.104s)
   Distributed NumPy (no Arrow): 1.720s across 11 partitions

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
   Convert (Arrow): 0.210s; transform: 0.001s; forecast: 0.048s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.204s; forecast(spark, 36 steps): 0.750s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 600,000, time: 0.497s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.259s  (convert=0.210s, tf=0.001s, fc=0.048s, numba=True)
   pandas-on-Spark total: 0.953s (tf=0.204s, fc=0.750s)
   Distributed NumPy (no Arrow): 0.497s across 11 partitions

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
   Convert (Arrow): 0.436s; transform: 0.001s; forecast: 0.025s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.853s; forecast(spark, 24 steps): 2.417s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 400,000, time: 0.400s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.462s  (convert=0.436s, tf=0.001s, fc=0.025s, numba=True)
   pandas-on-Spark total: 3.270s (tf=0.853s, fc=2.417s)
   Distributed NumPy (no Arrow): 0.400s across 11 partitions

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
   Convert (Arrow): 0.283s; transform: 0.005s; forecast: 0.041s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.144s; forecast(spark, 12 steps): 0.430s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 2,000,000, time: 1.144s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.328s  (convert=0.283s, tf=0.005s, fc=0.041s, numba=True)
   pandas-on-Spark total: 0.573s (tf=0.144s, fc=0.430s)
   Distributed NumPy (no Arrow): 1.144s across 11 partitions

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.
```

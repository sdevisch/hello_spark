# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 01:59 UTC

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
   Convert (Arrow): 0.456s; transform: 0.186s; forecast: 0.195s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.215s; forecast(spark, 48 steps): 1.146s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 300,000, time: 1.599s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.837s  (convert=0.456s, tf=0.186s, fc=0.195s, numba=True)
   pandas-on-Spark total: 1.361s (tf=0.215s, fc=1.146s)
   Distributed NumPy (no Arrow): 1.599s across 11 partitions

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
   Convert (Arrow): 0.183s; transform: 0.001s; forecast: 0.048s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.196s; forecast(spark, 36 steps): 0.755s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 600,000, time: 0.596s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.232s  (convert=0.183s, tf=0.001s, fc=0.048s, numba=True)
   pandas-on-Spark total: 0.951s (tf=0.196s, fc=0.755s)
   Distributed NumPy (no Arrow): 0.596s across 11 partitions

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
   Convert (Arrow): 0.454s; transform: 0.002s; forecast: 0.023s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.814s; forecast(spark, 24 steps): 2.348s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 400,000, time: 0.376s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.479s  (convert=0.454s, tf=0.002s, fc=0.023s, numba=True)
   pandas-on-Spark total: 3.163s (tf=0.814s, fc=2.348s)
   Distributed NumPy (no Arrow): 0.376s across 11 partitions

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
   Convert (Arrow): 0.357s; transform: 0.005s; forecast: 0.043s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.267s; forecast(spark, 12 steps): 0.435s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 2,000,000, time: 1.066s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.404s  (convert=0.357s, tf=0.005s, fc=0.043s, numba=True)
   pandas-on-Spark total: 0.702s (tf=0.267s, fc=0.435s)
   Distributed NumPy (no Arrow): 1.066s across 11 partitions

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.
```

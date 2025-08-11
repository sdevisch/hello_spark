# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 01:25 UTC

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
   Convert (Arrow): 0.516s; transform: 0.196s; forecast: 0.192s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.248s; forecast(spark, 48 steps): 1.126s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 300,000, time: 1.646s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.904s  (convert=0.516s, tf=0.196s, fc=0.192s, numba=True)
   pandas-on-Spark total: 1.374s (tf=0.248s, fc=1.126s)
   Distributed NumPy (no Arrow): 1.646s across 11 partitions

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
   Convert (Arrow): 0.183s; transform: 0.001s; forecast: 0.044s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.156s; forecast(spark, 36 steps): 0.766s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 600,000, time: 0.590s, mean(y)=0.9988

📊 Scenario summary:
   Package path total: 0.228s  (convert=0.183s, tf=0.001s, fc=0.044s, numba=True)
   pandas-on-Spark total: 0.922s (tf=0.156s, fc=0.766s)
   Distributed NumPy (no Arrow): 0.590s across 11 partitions

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
   Convert (Arrow): 0.424s; transform: 0.001s; forecast: 0.026s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.839s; forecast(spark, 24 steps): 2.323s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 400,000, time: 0.389s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.451s  (convert=0.424s, tf=0.001s, fc=0.026s, numba=True)
   pandas-on-Spark total: 3.163s (tf=0.839s, fc=2.323s)
   Distributed NumPy (no Arrow): 0.389s across 11 partitions

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
   Convert (Arrow): 0.343s; transform: 0.004s; forecast: 0.038s

== Spark path (pandas-like logic via Spark SQL functions) ==
   transform(spark): 0.326s; forecast(spark, 12 steps): 0.454s

== Distributed NumPy (no Arrow): mapPartitions on executors ==
   partitions: 11, rows: 2,000,000, time: 1.221s, mean(y)=0.9989

📊 Scenario summary:
   Package path total: 0.385s  (convert=0.343s, tf=0.004s, fc=0.038s, numba=True)
   pandas-on-Spark total: 0.780s (tf=0.326s, fc=0.454s)
   Distributed NumPy (no Arrow): 1.221s across 11 partitions

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.
```

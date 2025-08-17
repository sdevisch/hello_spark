# Performance 03: withColumn vs select (Arrow on/off, time and memory)

Generated: 2025-08-17 00:21 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
=== withColumn vs select: performance and memory ===
Spark version: 3.3.4
Rows: 100,000
withColumn_chain -> toPandas | rows=100,000 | arrow=False | time=1.95s | rssΔ=97.77MB
withColumn_chain -> toPandas | rows=100,000 | arrow=True | time=0.31s | rssΔ=15.38MB
select_combined -> toPandas | rows=100,000 | arrow=True | time=0.14s | rssΔ=10.64MB
select_combined -> toPandas | rows=100,000 | arrow=False | time=0.39s | rssΔ=14.69MB

Summary:
Scenario                         Arrow         Rows   Time (s)   RSS Δ (MB)
--------------------------------------------------------------------------------
withColumn_chain -> toPandas     False      100,000       1.95        97.77
withColumn_chain -> toPandas     True       100,000       0.31        15.38
select_combined -> toPandas      True       100,000       0.14        10.64
select_combined -> toPandas      False      100,000       0.39        14.69
```

# Performance 03: withColumn vs select (Arrow on/off, time and memory)

Generated: 2025-08-17 02:06 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
=== withColumn vs select: performance and memory ===
Spark version: 3.3.4
Row sizes: ['50,000', '100,000', '300,000']

--- Running scenarios for rows=50,000 ---
withColumn_chain -> toPandas | rows=50,000 | arrow=False | time=1.63s | rssΔ=65.36MB
withColumn_chain -> toPandas | rows=50,000 | arrow=True | time=0.31s | rssΔ=5.95MB
select_combined -> toPandas | rows=50,000 | arrow=True | time=0.18s | rssΔ=6.16MB
select_combined -> toPandas | rows=50,000 | arrow=False | time=0.18s | rssΔ=13.45MB

--- Running scenarios for rows=100,000 ---
withColumn_chain -> toPandas | rows=100,000 | arrow=False | time=0.36s | rssΔ=21.70MB
withColumn_chain -> toPandas | rows=100,000 | arrow=True | time=0.26s | rssΔ=15.69MB
select_combined -> toPandas | rows=100,000 | arrow=True | time=0.26s | rssΔ=9.14MB
select_combined -> toPandas | rows=100,000 | arrow=False | time=0.32s | rssΔ=8.59MB

--- Running scenarios for rows=300,000 ---
withColumn_chain -> toPandas | rows=300,000 | arrow=False | time=0.93s | rssΔ=65.81MB
withColumn_chain -> toPandas | rows=300,000 | arrow=True | time=0.25s | rssΔ=28.83MB
select_combined -> toPandas | rows=300,000 | arrow=True | time=0.15s | rssΔ=26.45MB
select_combined -> toPandas | rows=300,000 | arrow=False | time=0.84s | rssΔ=13.58MB

Summary:
Scenario                         Arrow         Rows   Time (s)   RSS Δ (MB)
--------------------------------------------------------------------------------
withColumn_chain -> toPandas     False       50,000       1.63        65.36
withColumn_chain -> toPandas     True        50,000       0.31         5.95
select_combined -> toPandas      True        50,000       0.18         6.16
select_combined -> toPandas      False       50,000       0.18        13.45
withColumn_chain -> toPandas     False      100,000       0.36        21.70
withColumn_chain -> toPandas     True       100,000       0.26        15.69
select_combined -> toPandas      True       100,000       0.26         9.14
select_combined -> toPandas      False      100,000       0.32         8.59
withColumn_chain -> toPandas     False      300,000       0.93        65.81
withColumn_chain -> toPandas     True       300,000       0.25        28.83
select_combined -> toPandas      True       300,000       0.15        26.45
select_combined -> toPandas      False      300,000       0.84        13.58
```

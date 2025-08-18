# Performance 03: withColumn vs select (JVM compute only)

Generated: 2025-08-18 19:35 UTC

## Scope

withColumn vs select: JVM compute only; no pandas/Arrow; materialized via aggregate sum of the last derived column.

## Console output

```text
=== withColumn vs select: JVM compute (agg sum of last column) ===
Spark version: 3.3.4
Row sizes: ['100,000', '300,000']

--- Running scenarios for rows=100,000 ---
withColumn_chain | rows=100,000 | action=sum(j) | time=0.99s
select_combined | rows=100,000 | action=sum(j) | time=0.13s
Summary | rows=100,000 | withColumn_chain=0.99s | select_combined=0.13s | speedup=7.6x

--- Running scenarios for rows=300,000 ---
withColumn_chain | rows=300,000 | action=sum(j) | time=0.17s
select_combined | rows=300,000 | action=sum(j) | time=0.13s
Summary | rows=300,000 | withColumn_chain=0.17s | select_combined=0.13s | speedup=1.3x

Done.
```

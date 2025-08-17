# Performance 03: withColumn vs select (JVM compute only)

Generated: 2025-08-17 04:06 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
=== withColumn vs select: JVM compute (agg sum of last column) ===
Spark version: 3.3.4
Row sizes: ['40,000,000']
Derived columns: 200

--- Running scenarios for rows=40,000,000 ---
withColumn_chain | rows=40,000,000 | parts=2000 | bytes≈3.8MB | write=13.98s | sum(read)=1.30s | total=15.28s
select_combined | rows=40,000,000 | parts=2000 | bytes≈3.8MB | write=10.00s | sum(read)=0.87s | total=10.88s
Summary | rows=40,000,000 | withColumn_chain=15.28s | select_combined=10.88s | speedup=1.4x

Why select can be faster here:
- select composes one expression tree for all derived columns, so Catalyst/codegen emits a single, tight kernel.
- withColumn chaining introduces many intermediate aliases and Projects; the optimizer can fold them, but analysis/codegen overhead can be higher.
- Both compute in the JVM. Differences mainly come from expression composition, plan size, and codegen, not from Arrow or Python.

Done.
```

# Performance 04: Spark 3.3 AQE – adaptive coalescing, advisory sizing, and skew handling

Generated: 2025-08-18 13:32 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
=== Building baseline (Spark 2.4-like): AQE OFF ===
Rows: 2,000,000; partitions: 91 (from persisted base)

--- Baseline plan (simple plan) ---
== Physical Plan ==
*(2) HashAggregate(keys=[k#14L], functions=[sum(v#15L)])
+- Exchange hashpartitioning(k#14L, 400), ENSURE_REQUIREMENTS, [plan_id=51]
   +- *(1) HashAggregate(keys=[k#14L], functions=[partial_sum(v#15L)])
      +- *(1) ColumnarToRow
         +- FileScan parquet [k#14L,v#15L] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp141owf1d/base..., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<k:bigint,v:bigint>


Baseline (AQE OFF) groupBy time: 0.84s

=== Enable AQE coalescePartitions (Spark 3.3) ===

--- AQE coalesce plan (simple plan) ---
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[k#41L], functions=[sum(v#42L)])
   +- Exchange hashpartitioning(k#41L, 400), ENSURE_REQUIREMENTS, [plan_id=132]
      +- HashAggregate(keys=[k#41L], functions=[partial_sum(v#42L)])
         +- FileScan parquet [k#41L,v#42L] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp141owf1d/base..., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<k:bigint,v:bigint>


AQE coalesce groupBy time: 0.38s

=== AQE: set advisoryPartitionSizeInBytes=64m (guides coalescing) ===

--- AQE advisory 64m plan (simple plan) ---
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[k#67L], functions=[sum(v#68L)])
   +- Exchange hashpartitioning(k#67L, 400), ENSURE_REQUIREMENTS, [plan_id=235]
      +- HashAggregate(keys=[k#67L], functions=[partial_sum(v#68L)])
         +- FileScan parquet [k#67L,v#68L] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp141owf1d/base..., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<k:bigint,v:bigint>


AQE advisory=64m groupBy time: 0.28s

=== AQE: skew join mitigation demo ===

--- Join baseline plan (simple plan) ---
== Physical Plan ==
*(3) HashAggregate(keys=[k#99L], functions=[sum((v#100L * w#95L))])
+- Exchange hashpartitioning(k#99L, 400), ENSURE_REQUIREMENTS, [plan_id=388]
   +- *(2) HashAggregate(keys=[k#99L], functions=[partial_sum((v#100L * w#95L))])
      +- *(2) Project [k#99L, v#100L, w#95L]
         +- *(2) BroadcastHashJoin [k#99L], [k#94L], Inner, BuildRight, false
            :- *(2) Filter isnotnull(k#99L)
            :  +- *(2) ColumnarToRow
            :     +- FileScan parquet [k#99L,v#100L] Batched: true, DataFilters: [isnotnull(k#99L)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp141owf1d/base..., PartitionFilters: [], PushedFilters: [IsNotNull(k)], ReadSchema: struct<k:bigint,v:bigint>
            +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]),false), [plan_id=382]
               +- *(1) Project [id#92L AS k#94L, ((id#92L * 2) + 3) AS w#95L]
                  +- *(1) Range (0, 1000, step=1, splits=11)


Join baseline time (AQE OFF): 0.77s

--- Join AQE skew plan (simple plan) ---
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[k#99L], functions=[sum((v#100L * w#95L))])
   +- Exchange hashpartitioning(k#99L, 400), ENSURE_REQUIREMENTS, [plan_id=568]
      +- HashAggregate(keys=[k#99L], functions=[partial_sum((v#100L * w#95L))])
         +- Project [k#99L, v#100L, w#95L]
            +- BroadcastHashJoin [k#99L], [k#94L], Inner, BuildRight, false
               :- Filter isnotnull(k#99L)
               :  +- FileScan parquet [k#99L,v#100L] Batched: true, DataFilters: [isnotnull(k#99L)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[file:/var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp141owf1d/base..., PartitionFilters: [], PushedFilters: [IsNotNull(k)], ReadSchema: struct<k:bigint,v:bigint>
               +- BroadcastExchange HashedRelationBroadcastMode(List(input[0, bigint, false]),false), [plan_id=563]
                  +- Project [id#92L AS k#94L, ((id#92L * 2) + 3) AS w#95L]
                     +- Range (0, 1000, step=1, splits=11)


Join AQE skew enabled time: 0.36s

Narration:
- AQE coalescing reduces the number of post-shuffle partitions, cutting scheduler and small-task overheads.
- Advisory partition sizing guides AQE toward fewer, larger partitions for better throughput.
- Skew join splits heavy partitions, preventing long stragglers and improving end-to-end time.
```

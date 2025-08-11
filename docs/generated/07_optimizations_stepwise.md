# Frameworks: Stepwise optimizations for model scoring

Generated: 2025-08-11 02:20 UTC

## Console output

```text
🚀 Stepwise optimization experiment
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
rows=600,000, entities=1,000, horizon=36, wide=100

== Baseline: naive Spark with iterative withColumn loops ==
   time: 1.555s

== Step 1: Project needed columns early ==
   time: 1.200s  (delta vs baseline: -0.355s)

== Step 2: Repartition by entity_id and sort within partitions ==
   time: 1.076s  (delta vs step1: -0.124s)

== Step 3a: Grouped Pandas UDF per entity (float64) with Arrow ==
/Users/sdevisch/repos/hello_spark/.venv311/lib/python3.11/site-packages/pyspark/sql/pandas/group_ops.py:104: UserWarning: It is preferred to use 'applyInPandas' over this API. This API will be deprecated in the future releases. See SPARK-28264 for more details.
  warnings.warn(
   time: 2.425s  (delta vs step2: +1.349s)

== Step 3b: Grouped Pandas UDF per entity (float32) with Arrow ==
   time: 0.638s  (delta vs 3a: -1.787s)

🏁 Summary (lower is better):
   Baseline (naive):   1.555s
   Step 1 (project):  1.200s
   Step 2 (partition):1.076s
   Step 3a (gp udf64):2.425s
   Step 3b (gp udf32):0.638s
```

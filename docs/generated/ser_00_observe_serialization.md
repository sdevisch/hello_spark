# Serialization 00: Using explain() and diagnostics

Generated: 2025-08-10 16:54 UTC

## Scope

Observe where Python shows up (explain/UI) and how to spot serialization.

## Console output

```text
🔍 Starting Serialization Observation Demo...
📚 Docs index: docs/index.md
🔍 OBSERVING SERIALIZATION IN SPARK
==================================================
🌐 Spark UI: http://localhost:4040
==================================================

==================================================
📋 DEMO 1: BASIC EXPLAIN() USAGE
==================================================
📊 Creating 50,000 rows of sample data...

🔍 1. Simple transformation (no UDF):

📊 Execution Plan:
== Parsed Logical Plan ==
'Project ['id, ('value * 2) AS doubled#7]
+- Project [id#0L, cast((rand(-958240777700817968) * cast(100 as double)) as int) AS value#2, CASE WHEN ((id#0L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#3]
   +- Range (0, 50000, step=1, splits=Some(11))

== Analyzed Logical Plan ==
id: bigint, doubled: int
Project [id#0L, (value#2 * 2) AS doubled#7]
+- Project [id#0L, cast((rand(-958240777700817968) * cast(100 as double)) as int) AS value#2, CASE WHEN ((id#0L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#3]
   +- Range (0, 50000, step=1, splits=Some(11))

== Optimized Logical Plan ==
Project [id#0L, (value#2 * 2) AS doubled#7]
+- Project [id#0L, cast((rand(-958240777700817968) * 100.0) as int) AS value#2]
   +- Range (0, 50000, step=1, splits=Some(11))

== Physical Plan ==
*(1) Project [id#0L, (value#2 * 2) AS doubled#7]
+- *(1) Project [id#0L, cast((rand(-958240777700817968) * 100.0) as int) AS value#2]
   +- *(1) Range (0, 50000, step=1, splits=11)


--------------------------------------------------
🔍 2. With aggregation:

📊 Execution Plan:
== Parsed Logical Plan ==
'Aggregate ['category], ['category, avg('value) AS avg_value#14]
+- Project [id#0L, cast((rand(-958240777700817968) * cast(100 as double)) as int) AS value#2, CASE WHEN ((id#0L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#3]
   +- Range (0, 50000, step=1, splits=Some(11))

== Analyzed Logical Plan ==
category: string, avg_value: double
Aggregate [category#3], [category#3, avg(value#2) AS avg_value#14]
+- Project [id#0L, cast((rand(-958240777700817968) * cast(100 as double)) as int) AS value#2, CASE WHEN ((id#0L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#3]
   +- Range (0, 50000, step=1, splits=Some(11))

== Optimized Logical Plan ==
Aggregate [category#3], [category#3, avg(value#2) AS avg_value#14]
+- Project [cast((rand(-958240777700817968) * 100.0) as int) AS value#2, CASE WHEN ((id#0L % 2) = 0) THEN even ELSE odd END AS category#3]
   +- Range (0, 50000, step=1, splits=Some(11))

== Physical Plan ==
*(2) HashAggregate(keys=[category#3], functions=[avg(value#2)], output=[category#3, avg_value#14])
+- Exchange hashpartitioning(category#3, 200), ENSURE_REQUIREMENTS, [plan_id=29]
   +- *(1) HashAggregate(keys=[category#3], functions=[partial_avg(value#2)], output=[category#3, sum#19, count#20L])
      +- *(1) Project [cast((rand(-958240777700817968) * 100.0) as int) AS value#2, CASE WHEN ((id#0L % 2) = 0) THEN even ELSE odd END AS category#3]
         +- *(1) Range (0, 50000, step=1, splits=11)


💡 KEY OBSERVATIONS:
   - Notice the plan shows only Catalyst operations
   - No mention of Python or serialization
   - All operations happen in the JVM

==================================================
🐍 DEMO 2: UDF IN EXECUTION PLANS
==================================================
📊 Creating 50,000 rows of sample data...

🔍 Native Spark function execution plan:
== Parsed Logical Plan ==
'Project ['id, ('value * 2) AS doubled#30]
+- Project [id#23L, cast((rand(1939090698594385202) * cast(100 as double)) as int) AS value#25, CASE WHEN ((id#23L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#26]
   +- Range (0, 50000, step=1, splits=Some(11))

== Analyzed Logical Plan ==
id: bigint, doubled: int
Project [id#23L, (value#25 * 2) AS doubled#30]
+- Project [id#23L, cast((rand(1939090698594385202) * cast(100 as double)) as int) AS value#25, CASE WHEN ((id#23L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#26]
   +- Range (0, 50000, step=1, splits=Some(11))

== Optimized Logical Plan ==
Project [id#23L, (value#25 * 2) AS doubled#30]
+- Project [id#23L, cast((rand(1939090698594385202) * 100.0) as int) AS value#25]
   +- Range (0, 50000, step=1, splits=Some(11))

== Physical Plan ==
*(1) Project [id#23L, (value#25 * 2) AS doubled#30]
+- *(1) Project [id#23L, cast((rand(1939090698594385202) * 100.0) as int) AS value#25]
   +- *(1) Range (0, 50000, step=1, splits=11)


--------------------------------------------------
🔍 Python UDF execution plan:
== Parsed Logical Plan ==
'Project ['id, python_double('value)#33 AS doubled#34]
+- Project [id#23L, cast((rand(1939090698594385202) * cast(100 as double)) as int) AS value#25, CASE WHEN ((id#23L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#26]
   +- Range (0, 50000, step=1, splits=Some(11))

== Analyzed Logical Plan ==
id: bigint, doubled: int
Project [id#23L, python_double(value#25)#33 AS doubled#34]
+- Project [id#23L, cast((rand(1939090698594385202) * cast(100 as double)) as int) AS value#25, CASE WHEN ((id#23L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#26]
   +- Range (0, 50000, step=1, splits=Some(11))

== Optimized Logical Plan ==
Project [id#23L, pythonUDF0#37 AS doubled#34]
+- BatchEvalPython [python_double(value#25)#33], [pythonUDF0#37]
   +- Project [id#23L, cast((rand(1939090698594385202) * 100.0) as int) AS value#25]
      +- Range (0, 50000, step=1, splits=Some(11))

== Physical Plan ==
*(2) Project [id#23L, pythonUDF0#37 AS doubled#34]
+- BatchEvalPython [python_double(value#25)#33], [pythonUDF0#37]
   +- *(1) Project [id#23L, cast((rand(1939090698594385202) * 100.0) as int) AS value#25]
      +- *(1) Range (0, 50000, step=1, splits=11)


💡 KEY OBSERVATIONS:
   - UDF plans show 'BatchEvalPython' or similar
   - This indicates data serialization to Python
   - Much more complex execution plan
   - Serialization happens at the BatchEvalPython stage

==================================================
⏱️  DEMO 3: TIMING WITH EXPLAIN ANALYSIS
==================================================
📊 Creating 100,000 rows of sample data...

🚀 1. Native Spark function:
   Execution plan with timing:
   ✅ Processed 100,000 rows in 0.774s
== Physical Plan ==
* Project (3)
+- * Project (2)
   +- * Range (1)


(1) Range [codegen id : 1]
Output [1]: [id#38L]
Arguments: Range (0, 100000, step=1, splits=Some(11))

(2) Project [codegen id : 1]
Output [2]: [id#38L, cast((rand(-7326776541570372847) * 100.0) as int) AS value#40]
Input [1]: [id#38L]

(3) Project [codegen id : 1]
Output [2]: [id#38L, cast(SQRT(cast(value#40 as double)) as int) AS result#45]
Input [2]: [id#38L, value#40]



🐍 2. Python UDF:
   Execution plan with timing:
   ✅ Processed 100,000 rows in 0.063s
== Physical Plan ==
* Project (4)
+- BatchEvalPython (3)
   +- * Project (2)
      +- * Range (1)


(1) Range [codegen id : 1]
Output [1]: [id#38L]
Arguments: Range (0, 100000, step=1, splits=Some(11))

(2) Project [codegen id : 1]
Output [2]: [id#38L, cast((rand(-7326776541570372847) * 100.0) as int) AS value#40]
Input [1]: [id#38L]

(3) BatchEvalPython
Input [2]: [id#38L, value#40]
Arguments: [complex_calc(value#40)#48], [pythonUDF0#66]

(4) Project [codegen id : 2]
Output [2]: [id#38L, pythonUDF0#66 AS result#49]
Input [3]: [id#38L, value#40, pythonUDF0#66]



📈 PERFORMANCE COMPARISON:
   Native Spark: 0.774s
   Python UDF:   0.063s
   Speedup:      0.1x faster with native

==================================================
🎯 DEMO 4: IDENTIFYING SERIALIZATION POINTS
==================================================
📊 Creating 80,000 rows of sample data...

🔍 Complex query with mixed operations:

📊 Full execution plan:
== Parsed Logical Plan ==
'Aggregate ['category_python], ['category_python, avg('value) AS avg_value#89, avg('value_squared) AS avg_squared#91, count(1) AS count#93L]
+- Project [id#67L, value#69, category_python#75, (value#69 * value#69) AS value_squared#79]
   +- Project [id#67L, value#69, categorize_value(value#69)#74 AS category_python#75]
      +- Filter (value#69 > 10)
         +- Project [id#67L, cast((rand(1724659738247840045) * cast(100 as double)) as int) AS value#69, CASE WHEN ((id#67L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#70]
            +- Range (0, 80000, step=1, splits=Some(11))

== Analyzed Logical Plan ==
category_python: string, avg_value: double, avg_squared: double, count: bigint
Aggregate [category_python#75], [category_python#75, avg(value#69) AS avg_value#89, avg(value_squared#79) AS avg_squared#91, count(1) AS count#93L]
+- Project [id#67L, value#69, category_python#75, (value#69 * value#69) AS value_squared#79]
   +- Project [id#67L, value#69, categorize_value(value#69)#74 AS category_python#75]
      +- Filter (value#69 > 10)
         +- Project [id#67L, cast((rand(1724659738247840045) * cast(100 as double)) as int) AS value#69, CASE WHEN ((id#67L % cast(2 as bigint)) = cast(0 as bigint)) THEN even ELSE odd END AS category#70]
            +- Range (0, 80000, step=1, splits=Some(11))

== Optimized Logical Plan ==
Aggregate [category_python#75], [category_python#75, avg(value#69) AS avg_value#89, avg(value_squared#79) AS avg_squared#91, count(1) AS count#93L]
+- Project [value#69, pythonUDF0#98 AS category_python#75, (value#69 * value#69) AS value_squared#79]
   +- BatchEvalPython [categorize_value(value#69)#74], [pythonUDF0#98]
      +- Filter (isnotnull(value#69) AND (value#69 > 10))
         +- Project [cast((rand(1724659738247840045) * 100.0) as int) AS value#69]
            +- Range (0, 80000, step=1, splits=Some(11))

== Physical Plan ==
*(3) HashAggregate(keys=[category_python#75], functions=[avg(value#69), avg(value_squared#79), count(1)], output=[category_python#75, avg_value#89, avg_squared#91, count#93L])
+- Exchange hashpartitioning(category_python#75, 200), ENSURE_REQUIREMENTS, [plan_id=193]
   +- *(2) HashAggregate(keys=[category_python#75], functions=[partial_avg(value#69), partial_avg(value_squared#79), partial_count(1)], output=[category_python#75, sum#104, count#105L, sum#106, count#107L, count#108L])
      +- *(2) Project [value#69, pythonUDF0#98 AS category_python#75, (value#69 * value#69) AS value_squared#79]
         +- BatchEvalPython [categorize_value(value#69)#74], [pythonUDF0#98]
            +- *(1) Filter (isnotnull(value#69) AND (value#69 > 10))
               +- *(1) Project [cast((rand(1724659738247840045) * 100.0) as int) AS value#69]
                  +- *(1) Range (0, 80000, step=1, splits=11)


⏱️  Execution time: 1.157s

🔍 Results:
   Row(category_python='low', avg_value=17.521958562068356, avg_squared=323.28572693465554, count=11294)
   Row(category_python='high', avg_value=87.0208312468703, avg_squared=7624.9532298447675, count=19970)
   Row(category_python='medium', avg_value=49.49725529514977, avg_squared=2656.324777541045, count=39895)

💡 SERIALIZATION IDENTIFICATION:
   1. Look for 'BatchEvalPython' in the plan
   2. This shows exactly where Python UDF runs
   3. Data flows: JVM → Python → JVM at this point
   4. All operations before/after are pure Spark

==================================================
🌐 DEMO 5: SPARK UI OBSERVATION
==================================================
📊 Creating 150,000 rows of sample data...

🚀 Running operation with UDF...
   👀 Open Spark UI: http://localhost:4040
   📊 Go to 'SQL' tab to see query details
   🔍 Look for stages with 'Python' in the description

✅ Processed 150,000 rows in 0.081s

🔍 WHAT TO LOOK FOR IN SPARK UI:
   1. 'SQL' tab → Click on the query
   2. Look for stages with 'BatchEvalPython'
   3. These stages show serialization overhead
   4. Compare timing with pure Spark stages
   5. 'Details' show the full execution plan

==================================================
🛠️  DEMO 6: SIMPLE DIAGNOSTIC TOOLS
==================================================
📊 Creating 100,000 rows of sample data...

📊 Tool 1: explain('cost') - shows cost-based optimization:
== Optimized Logical Plan ==
Filter (isnotnull(value#133) AND (value#133 > 50)), Statistics(sizeInBytes=976.6 KiB)
+- Project [id#131L, cast((rand(-2394778090245226580) * 100.0) as int) AS value#133], Statistics(sizeInBytes=976.6 KiB)
   +- Range (0, 100000, step=1, splits=Some(11)), Statistics(sizeInBytes=781.3 KiB, rowCount=1.00E+5)

== Physical Plan ==
*(1) Filter (isnotnull(value#133) AND (value#133 > 50))
+- *(1) Project [id#131L, cast((rand(-2394778090245226580) * 100.0) as int) AS value#133]
   +- *(1) Range (0, 100000, step=1, splits=11)



📊 Tool 2: show() vs collect() performance:
   show() output:
+---+-------+
| id|doubled|
+---+-------+
|  0|    102|
|  1|    106|
|  2|     86|
|  3|    158|
|  4|    160|
+---+-------+
only showing top 5 rows


⏱️  show() time: 0.121s
   collect() time: 0.076s

📊 Tool 3: Cache impact on UDF performance:
   First access (cache miss): 0.256s
   Second access (cache hit): 0.022s
   Cache speedup: 11.4x

==================================================
🎉 ALL SERIALIZATION OBSERVATION DEMOS COMPLETED!
==================================================

🎯 KEY TAKEAWAYS FOR OBSERVING SERIALIZATION:
1. 🔍 Use explain() to see execution plans
2. 👀 Look for 'BatchEvalPython' in plans (= serialization)
3. ⏱️  Time operations to measure serialization overhead
4. 🌐 Use Spark UI SQL tab to see detailed query execution
5. 🛠️  Use explain('formatted') for readable plans
6. 📊 Compare native vs UDF execution plans side-by-side

🌐 Keep exploring: http://localhost:4040
   Go to SQL tab → Click queries → See execution details

⏳ Skipping 30s keep-alive for docs generation

🧹 Cleaning up...
   ✅ Stopped Spark session

👋 Serialization observation demo completed!
```

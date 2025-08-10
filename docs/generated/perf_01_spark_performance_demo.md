# Performance 01: I/O, serialization, caching, partitions, joins, persistence

Generated: 2025-08-10 17:01 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
🚀 Starting Spark Performance Demo...
📚 Docs index: docs/index.md
📁 Temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmpvfq17myw
🌐 Spark UI: http://localhost:4040
============================================================
🚀 SPARK PERFORMANCE DEMONSTRATION
============================================================
This demo will show common performance bottlenecks and solutions
Watch the Spark UI at http://localhost:4040 for detailed metrics!

============================================================
🗂️  DEMO 1: FILE FORMAT PERFORMANCE
============================================================

📊 Generating 100,000 rows of sample data...

⏱️  Timing: SLOW - Writing CSV
   ✅ Completed in 1.40s

⏱️  Timing: SLOW - Reading CSV
   ✅ Completed in 0.94s (processed 99,989 rows)

⏱️  Timing: FAST - Writing Parquet
   ✅ Completed in 0.83s

⏱️  Timing: FAST - Reading Parquet
   ✅ Completed in 0.21s (processed 100,000 rows)

📈 RESULTS:
   CSV Total Time:     2.33s
   Parquet Total Time: 1.04s
   Speedup: 2.2x faster

============================================================
🐍 DEMO 2: SERIALIZATION ISSUES (Python UDFs)
============================================================

📊 Generating 500,000 rows of sample data...

⏱️  Timing: SLOW - Python UDF with serialization
   ✅ Completed in 0.11s (processed 500,000 rows)

⏱️  Timing: FAST - Native Spark functions
   ✅ Completed in 0.05s (processed 500,000 rows)

📈 RESULTS:
   Python UDF Time:    0.11s
   Native Spark Time:  0.05s
   Speedup: 2.1x faster
   💡 Tip: Use built-in Spark functions instead of Python UDFs!

============================================================
💾 DEMO 3: CACHING AND PERSISTENCE STRATEGIES
============================================================

📊 Generating 800,000 rows of sample data...

🐌 SLOW: No caching - recomputing transformations

⏱️  Timing: SLOW - First computation (no cache)
   ✅ Completed in 0.41s (processed 2 rows)

⏱️  Timing: SLOW - Second computation (no cache)
   ✅ Completed in 0.23s (processed 2 rows)

🚀 FAST: With caching - compute once, reuse multiple times

⏱️  Timing: FAST - First computation (with cache)
   ✅ Completed in 0.35s (processed 2 rows)

⏱️  Timing: FAST - Second computation (from cache)
   ✅ Completed in 0.06s (processed 2 rows)

📈 RESULTS:
   No Cache Total Time:   0.64s
   With Cache Total Time: 0.40s
   Speedup: 1.6x faster
   💡 Tip: Cache DataFrames that are used multiple times!

============================================================
🗂️  DEMO 4: PARTITIONING STRATEGIES
============================================================

📊 Generating 1,000,000 rows of sample data...

🐌 SLOW: Too many small partitions

⏱️  Timing: SLOW - Over-partitioned aggregation
   ✅ Completed in 2.45s (processed 2 rows)

🚀 FAST: Optimal partitioning

⏱️  Timing: FAST - Optimally partitioned aggregation
   ✅ Completed in 0.37s (processed 2 rows)

📈 RESULTS:
   Over-partitioned Time:  2.45s
   Optimal partition Time: 0.37s
   Speedup: 6.6x faster
   💡 Tip: Use 2-3 partitions per CPU core for optimal performance!

============================================================
📡 DEMO 5: BROADCAST VS SHUFFLE JOINS
============================================================

📊 Generating 500,000 rows of sample data...
📊 Large dataset: 500,000 rows
📊 Small dataset: 2 rows

🐌 SLOW: Regular join (shuffle)

⏱️  Timing: SLOW - Shuffle join
   ✅ Completed in 0.41s (processed 500,000 rows)

🚀 FAST: Broadcast join

⏱️  Timing: FAST - Broadcast join
   ✅ Completed in 0.25s (processed 500,000 rows)

📈 RESULTS:
   Shuffle Join Time:   0.41s
   Broadcast Join Time: 0.25s
   Speedup: 1.7x faster
   💡 Tip: Broadcast small tables (< 10MB) to avoid shuffles!

============================================================
🧠 DEMO 6: MEMORY MANAGEMENT & PERSISTENCE
============================================================

📊 Generating 300,000 rows of sample data...
❌ Error during demo: type object 'StorageLevel' has no attribute 'MEMORY_ONLY_SER'

⏳ Skipping 60s keep-alive for docs generation

🧹 Cleaning up...
   ✅ Removed temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmpvfq17myw
   ✅ Stopped Spark session

👋 Demo completed!
```

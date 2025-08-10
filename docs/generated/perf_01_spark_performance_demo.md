# Performance 01: I/O, serialization, caching, partitions, joins, persistence

Generated: 2025-08-10 16:23 UTC

## Console output

```text
🚀 Starting Spark Performance Demo...
📁 Temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp3a6p1dda
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
   ✅ Completed in 1.39s

⏱️  Timing: SLOW - Reading CSV
   ✅ Completed in 0.91s (processed 99,989 rows)

⏱️  Timing: FAST - Writing Parquet
   ✅ Completed in 0.80s

⏱️  Timing: FAST - Reading Parquet
   ✅ Completed in 0.21s (processed 100,000 rows)

📈 RESULTS:
   CSV Total Time:     2.30s
   Parquet Total Time: 1.01s
   Speedup: 2.3x faster

============================================================
🐍 DEMO 2: SERIALIZATION ISSUES (Python UDFs)
============================================================

📊 Generating 500,000 rows of sample data...

⏱️  Timing: SLOW - Python UDF with serialization
   ✅ Completed in 0.09s (processed 500,000 rows)

⏱️  Timing: FAST - Native Spark functions
   ✅ Completed in 0.05s (processed 500,000 rows)

📈 RESULTS:
   Python UDF Time:    0.09s
   Native Spark Time:  0.05s
   Speedup: 1.9x faster
   💡 Tip: Use built-in Spark functions instead of Python UDFs!

============================================================
💾 DEMO 3: CACHING AND PERSISTENCE STRATEGIES
============================================================

📊 Generating 800,000 rows of sample data...

🐌 SLOW: No caching - recomputing transformations

⏱️  Timing: SLOW - First computation (no cache)
   ✅ Completed in 0.40s (processed 2 rows)

⏱️  Timing: SLOW - Second computation (no cache)
   ✅ Completed in 0.23s (processed 2 rows)

🚀 FAST: With caching - compute once, reuse multiple times

⏱️  Timing: FAST - First computation (with cache)
   ✅ Completed in 0.35s (processed 2 rows)

⏱️  Timing: FAST - Second computation (from cache)
   ✅ Completed in 0.05s (processed 2 rows)

📈 RESULTS:
   No Cache Total Time:   0.63s
   With Cache Total Time: 0.40s
   Speedup: 1.6x faster
   💡 Tip: Cache DataFrames that are used multiple times!

============================================================
🗂️  DEMO 4: PARTITIONING STRATEGIES
============================================================

📊 Generating 1,000,000 rows of sample data...

🐌 SLOW: Too many small partitions

⏱️  Timing: SLOW - Over-partitioned aggregation
   ✅ Completed in 2.22s (processed 2 rows)

🚀 FAST: Optimal partitioning

⏱️  Timing: FAST - Optimally partitioned aggregation
   ✅ Completed in 0.33s (processed 2 rows)

📈 RESULTS:
   Over-partitioned Time:  2.22s
   Optimal partition Time: 0.33s
   Speedup: 6.8x faster
   💡 Tip: Use 2-3 partitions per CPU core for optimal performance!

============================================================
📡 DEMO 5: BROADCAST VS SHUFFLE JOINS
============================================================

📊 Generating 500,000 rows of sample data...
📊 Large dataset: 500,000 rows
📊 Small dataset: 2 rows

🐌 SLOW: Regular join (shuffle)

⏱️  Timing: SLOW - Shuffle join
   ✅ Completed in 0.42s (processed 500,000 rows)

🚀 FAST: Broadcast join

⏱️  Timing: FAST - Broadcast join
   ✅ Completed in 0.21s (processed 500,000 rows)

📈 RESULTS:
   Shuffle Join Time:   0.42s
   Broadcast Join Time: 0.21s
   Speedup: 2.0x faster
   💡 Tip: Broadcast small tables (< 10MB) to avoid shuffles!

============================================================
🧠 DEMO 6: MEMORY MANAGEMENT & PERSISTENCE
============================================================

📊 Generating 300,000 rows of sample data...
❌ Error during demo: type object 'StorageLevel' has no attribute 'MEMORY_ONLY_SER'

⏳ Skipping 60s keep-alive for docs generation

🧹 Cleaning up...
   ✅ Removed temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmp3a6p1dda
   ✅ Stopped Spark session

👋 Demo completed!
```

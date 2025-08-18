# Performance 01: I/O, serialization, caching, partitions, joins, persistence

Generated: 2025-08-17 02:24 UTC

## Scope

Cross-cutting performance practices: IO formats, UDF vs native, caching, partitioning, broadcast, and data types.

## Console output

```text
🚀 Starting Spark Performance Demo...
📚 Docs index: docs/index.md
📁 Temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmpci7_8ecv
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
   ✅ Completed in 1.29s

⏱️  Timing: SLOW - Reading CSV
   ✅ Completed in 0.89s (processed 99,989 rows)

⏱️  Timing: FAST - Writing Parquet
   ✅ Completed in 0.85s

⏱️  Timing: FAST - Reading Parquet
   ✅ Completed in 0.18s (processed 100,000 rows)

📈 RESULTS:
   CSV Total Time:     2.18s
   Parquet Total Time: 1.03s
   Speedup: 2.1x faster

============================================================
🐍 DEMO 2: SERIALIZATION ISSUES (Python UDFs)
============================================================

📊 Generating 500,000 rows of sample data...

⏱️  Timing: SLOW - Python UDF with serialization
   ✅ Completed in 0.09s (processed 500,000 rows)

⏱️  Timing: FAST - Native Spark functions
   ✅ Completed in 0.06s (processed 500,000 rows)

📈 RESULTS:
   Python UDF Time:    0.09s
   Native Spark Time:  0.06s
   Speedup: 1.7x faster
   💡 Tip: Use built-in Spark functions instead of Python UDFs!

============================================================
💾 DEMO 3: CACHING AND PERSISTENCE STRATEGIES
============================================================

📊 Generating 800,000 rows of sample data...

🐌 SLOW: No caching - recomputing transformations

⏱️  Timing: SLOW - First computation (no cache)
   ✅ Completed in 0.36s (processed 2 rows)

⏱️  Timing: SLOW - Second computation (no cache)
   ✅ Completed in 0.22s (processed 2 rows)

🚀 FAST: With caching - compute once, reuse multiple times

⏱️  Timing: FAST - First computation (with cache)
   ✅ Completed in 0.49s (processed 2 rows)

⏱️  Timing: FAST - Second computation (from cache)
   ✅ Completed in 0.23s (processed 2 rows)

📈 RESULTS:
   No Cache Total Time:   0.58s
   With Cache Total Time: 0.72s
   Speedup: 0.8x faster
   💡 Tip: Cache DataFrames that are used multiple times!

============================================================
🗂️  DEMO 4: PARTITIONING STRATEGIES
============================================================

📊 Generating 1,000,000 rows of sample data...

🐌 SLOW: Too many small partitions

⏱️  Timing: SLOW - Over-partitioned aggregation
   ✅ Completed in 2.10s (processed 2 rows)

🚀 FAST: Optimal partitioning

⏱️  Timing: FAST - Optimally partitioned aggregation
   ✅ Completed in 0.50s (processed 2 rows)

📈 RESULTS:
   Over-partitioned Time:  2.10s
   Optimal partition Time: 0.50s
   Speedup: 4.2x faster
   💡 Tip: Use 2-3 partitions per CPU core for optimal performance!

============================================================
📡 DEMO 5: BROADCAST VS SHUFFLE JOINS
============================================================

📊 Generating 500,000 rows of sample data...
📊 Large dataset: 500,000 rows
📊 Small dataset: 2 rows

🐌 SLOW: Regular join (shuffle)

⏱️  Timing: SLOW - Shuffle join
   ✅ Completed in 0.35s (processed 500,000 rows)

🚀 FAST: Broadcast join

⏱️  Timing: FAST - Broadcast join
   ✅ Completed in 0.16s (processed 500,000 rows)

📈 RESULTS:
   Shuffle Join Time:   0.35s
   Broadcast Join Time: 0.16s
   Speedup: 2.2x faster
   💡 Tip: Broadcast small tables (< 10MB) to avoid shuffles!

============================================================
🧠 DEMO 6: MEMORY MANAGEMENT & PERSISTENCE
============================================================

📊 Generating 300,000 rows of sample data...

🧪 Testing MEMORY_ONLY persistence:

⏱️  Timing: MEMORY_ONLY - Initial caching
   ✅ Completed in 0.36s

⏱️  Timing: MEMORY_ONLY - Access from cache
   ✅ Completed in 0.07s

🧪 Testing MEMORY_AND_DISK persistence:

⏱️  Timing: MEMORY_AND_DISK - Initial caching
   ✅ Completed in 0.21s

⏱️  Timing: MEMORY_AND_DISK - Access from cache
   ✅ Completed in 0.05s

🧪 Testing DISK_ONLY persistence:

⏱️  Timing: DISK_ONLY - Initial caching
   ✅ Completed in 0.18s

⏱️  Timing: DISK_ONLY - Access from cache
   ✅ Completed in 0.07s

📈 PERSISTENCE STRATEGY COMPARISON:
Strategy             Cache Time   Access Time  Total     
------------------------------------------------------------
MEMORY_ONLY          0.36         0.07         0.43      
MEMORY_AND_DISK      0.21         0.05         0.26      
DISK_ONLY            0.18         0.07         0.25      

💡 Tips:
   - MEMORY_ONLY: Fastest but may cause OOM
   - MEMORY_AND_DISK: Good balance (recommended)
   - DISK_ONLY: Slowest but handles large datasets

============================================================
🎉 ALL DEMOS COMPLETED!
============================================================

🎯 KEY TAKEAWAYS:
1. 📁 Use Parquet instead of CSV for better I/O performance
2. 🐍 Avoid Python UDFs - use native Spark functions
3. 💾 Cache DataFrames that are accessed multiple times
4. 🗂️  Use optimal partitioning (2-3 partitions per CPU core)
5. 📡 Broadcast small tables to avoid expensive shuffles
6. 🧠 Choose appropriate persistence strategy for your use case

🌐 Spark UI: http://localhost:4040
   Check the 'SQL' and 'Jobs' tabs to see execution plans!

⏳ Skipping 60s keep-alive for docs generation

🧹 Cleaning up...
   ✅ Removed temp directory: /var/folders/yv/qzkfbsw13_q1kpm5kdb1qpx40000gn/T/tmpci7_8ecv
   ✅ Stopped Spark session

👋 Demo completed!
```

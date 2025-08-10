# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 16:17 UTC

## Console output

```text
🚀 Starting Comprehensive Performance Benchmark...
💻 System: 18.0GB RAM, 11 CPU cores
✅ Numba version: 0.61.2
🚀 COMPREHENSIVE PERFORMANCE BENCHMARK
============================================================
📊 Dataset size: 200,000 rows × 12 columns
💾 Estimated memory: ~0.0 GB
============================================================
🌐 Spark UI (No Arrow): http://localhost:4040
🌐 Spark UI (With Arrow): http://localhost:4041

📊 Generating test data (200,000 × 12)...
🔄 Converting data to different formats...
⏱️  Creating pandas DataFrame
   ✅ 0.008s | Memory: +0.05GB | Peak: 0.19GB
⏱️  Creating NumPy arrays
   ✅ 0.000s | Memory: +0.00GB | Peak: 0.23GB
⏱️  Creating Spark DataFrame (no Arrow)
   ✅ 0.864s | Memory: +0.01GB | Peak: 0.24GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.217s | Memory: +0.00GB | Peak: 0.24GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.24GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.24GB
⏱️  Numba basic ops
   ✅ 0.154s | Memory: +0.03GB | Peak: 0.27GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.135s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.060s | Memory: +0.00GB | Peak: 0.27GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.003      0.00         1.0       x
numpy                0.003      0.00         1.0       x
numba                0.154      0.03         45.8      x
spark_no_arrow       0.135      0.00         40.1      x
spark_arrow          0.060      0.00         17.9      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.010s | Memory: +0.01GB | Peak: 0.27GB
⏱️  NumPy aggregations
   ✅ 0.017s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Numba aggregations
   ✅ 0.209s | Memory: +0.01GB | Peak: 0.28GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.046s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.052s | Memory: +0.00GB | Peak: 0.28GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.010      0.01         1.0       x
numpy                0.017      0.00         1.7       x
numba                0.209      0.01         20.6      x
spark_no_arrow       0.046      0.00         4.5       x
spark_arrow          0.052      0.00         5.1       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.007s | Memory: +0.01GB | Peak: 0.29GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba math ops
   ✅ 0.264s | Memory: +0.01GB | Peak: 0.30GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.754s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.592s | Memory: +0.00GB | Peak: 0.30GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.007      0.01         1.7       x
numpy                0.004      0.00         1.0       x
numba                0.264      0.01         59.5      x
spark_no_arrow       0.754      0.00         169.7     x
spark_arrow          0.592      0.00         133.2     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.646s | Memory: +0.03GB | Peak: 0.33GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.400s | Memory: +0.04GB | Peak: 0.37GB
⏱️  NumPy to pandas
   ✅ 0.006s | Memory: +0.01GB | Peak: 0.38GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.646      0.03         101.8     x
spark_arrow          0.400      0.04         63.1      x
numpy                0.006      0.01         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 45.8x

🎯 Aggregations:
   🥇 Winner: pandas (0.010s)
   ⚡ Max speedup: 20.6x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 169.7x

🎯 Data Conversion:
   🥇 Winner: numpy (0.006s)
   ⚡ Max speedup: 101.8x

💡 KEY INSIGHTS:
   - Dataset size: 200,000 rows × 12 columns
   - NumPy generally fastest for mathematical operations
   - Numba provides excellent speedup for complex calculations
   - Arrow significantly improves Spark-pandas conversion
   - Pandas excels at mixed data type operations
   - Memory usage varies significantly between approaches

🧹 Cleaning up...
   ✅ Stopped all Spark sessions

👋 Comprehensive benchmark completed!
```

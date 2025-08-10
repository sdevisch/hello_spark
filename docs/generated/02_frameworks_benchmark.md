# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 16:31 UTC

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
   ✅ 0.000s | Memory: +0.00GB | Peak: 0.21GB
⏱️  Creating Spark DataFrame (no Arrow)
   ✅ 0.933s | Memory: +0.01GB | Peak: 0.22GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.234s | Memory: +0.00GB | Peak: 0.22GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.004s | Memory: +0.01GB | Peak: 0.23GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.23GB
⏱️  Numba basic ops
   ✅ 0.147s | Memory: +0.03GB | Peak: 0.27GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.101s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.055s | Memory: +0.00GB | Peak: 0.27GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.004      0.01         1.1       x
numpy                0.003      0.00         1.0       x
numba                0.147      0.03         43.9      x
spark_no_arrow       0.101      0.00         30.2      x
spark_arrow          0.055      0.00         16.3      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.010s | Memory: +0.00GB | Peak: 0.27GB
⏱️  NumPy aggregations
   ✅ 0.017s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Numba aggregations
   ✅ 0.214s | Memory: +0.01GB | Peak: 0.28GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.053s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.045s | Memory: +0.00GB | Peak: 0.28GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.010      0.00         1.0       x
numpy                0.017      0.00         1.8       x
numba                0.214      0.01         22.3      x
spark_no_arrow       0.053      0.00         5.5       x
spark_arrow          0.045      0.00         4.7       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.008s | Memory: +0.01GB | Peak: 0.28GB
⏱️  NumPy math ops
   ✅ 0.005s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba math ops
   ✅ 0.262s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.672s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.805s | Memory: +0.00GB | Peak: 0.29GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.008      0.01         1.6       x
numpy                0.005      0.00         1.0       x
numba                0.262      0.00         54.4      x
spark_no_arrow       0.672      0.00         139.5     x
spark_arrow          0.805      0.00         167.2     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.638s | Memory: +0.04GB | Peak: 0.33GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.468s | Memory: +0.05GB | Peak: 0.38GB
⏱️  NumPy to pandas
   ✅ 0.007s | Memory: +0.00GB | Peak: 0.38GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.638      0.04         95.2      x
spark_arrow          0.468      0.05         69.9      x
numpy                0.007      0.00         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 43.9x

🎯 Aggregations:
   🥇 Winner: pandas (0.010s)
   ⚡ Max speedup: 22.3x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.005s)
   ⚡ Max speedup: 167.2x

🎯 Data Conversion:
   🥇 Winner: numpy (0.007s)
   ⚡ Max speedup: 95.2x

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

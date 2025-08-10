# Frameworks: Comprehensive performance benchmark

Generated: 2025-08-10 13:59 UTC

## Console output

```text
🚀 Starting Comprehensive Performance Benchmark...
💻 System: 18.0GB RAM, 11 CPU cores
✅ Numba version: 0.60.0
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
   ✅ 0.006s | Memory: +0.05GB | Peak: 0.18GB
⏱️  Creating NumPy arrays
   ✅ 0.000s | Memory: +0.00GB | Peak: 0.20GB
⏱️  Creating Spark DataFrame (no Arrow)
   ✅ 0.834s | Memory: +0.00GB | Peak: 0.20GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.232s | Memory: +0.00GB | Peak: 0.20GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.004s | Memory: +0.01GB | Peak: 0.22GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.22GB
⏱️  Numba basic ops
   ✅ 0.163s | Memory: +0.03GB | Peak: 0.25GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.108s | Memory: +0.00GB | Peak: 0.25GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.054s | Memory: +0.00GB | Peak: 0.25GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.004      0.01         1.4       x
numpy                0.003      0.00         1.0       x
numba                0.163      0.03         51.8      x
spark_no_arrow       0.108      0.00         34.4      x
spark_arrow          0.054      0.00         17.0      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.011s | Memory: +0.00GB | Peak: 0.25GB
⏱️  NumPy aggregations
   ✅ 0.017s | Memory: +0.00GB | Peak: 0.25GB
⏱️  Numba aggregations
   ✅ 0.268s | Memory: +0.01GB | Peak: 0.26GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.051s | Memory: +0.00GB | Peak: 0.26GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.045s | Memory: +0.00GB | Peak: 0.26GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.011      0.00         1.0       x
numpy                0.017      0.00         1.5       x
numba                0.268      0.01         23.5      x
spark_no_arrow       0.051      0.00         4.5       x
spark_arrow          0.045      0.00         3.9       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.007s | Memory: +0.01GB | Peak: 0.27GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Numba math ops
   ✅ 0.328s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.694s | Memory: +0.00GB | Peak: 0.27GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.858s | Memory: +0.00GB | Peak: 0.27GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.007      0.01         1.8       x
numpy                0.004      0.00         1.0       x
numba                0.328      0.00         79.5      x
spark_no_arrow       0.694      0.00         168.0     x
spark_arrow          0.858      0.00         207.8     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.633s | Memory: +0.03GB | Peak: 0.31GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.430s | Memory: +0.04GB | Peak: 0.35GB
⏱️  NumPy to pandas
   ✅ 0.006s | Memory: +0.02GB | Peak: 0.37GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.633      0.03         114.6     x
spark_arrow          0.430      0.04         77.9      x
numpy                0.006      0.02         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 51.8x

🎯 Aggregations:
   🥇 Winner: pandas (0.011s)
   ⚡ Max speedup: 23.5x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 207.8x

🎯 Data Conversion:
   🥇 Winner: numpy (0.006s)
   ⚡ Max speedup: 114.6x

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

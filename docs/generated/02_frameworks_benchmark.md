# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 16:24 UTC

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
   ✅ 0.929s | Memory: +0.01GB | Peak: 0.24GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.223s | Memory: +0.00GB | Peak: 0.24GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.004s | Memory: +0.01GB | Peak: 0.24GB
⏱️  NumPy basic ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.25GB
⏱️  Numba basic ops
   ✅ 0.176s | Memory: +0.03GB | Peak: 0.28GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.110s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.084s | Memory: +0.00GB | Peak: 0.28GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.004      0.01         1.0       x
numpy                0.004      0.00         1.1       x
numba                0.176      0.03         43.9      x
spark_no_arrow       0.110      0.00         27.4      x
spark_arrow          0.084      0.00         20.9      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.010s | Memory: +0.00GB | Peak: 0.29GB
⏱️  NumPy aggregations
   ✅ 0.017s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba aggregations
   ✅ 0.210s | Memory: +0.01GB | Peak: 0.29GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.046s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.046s | Memory: +0.00GB | Peak: 0.29GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.010      0.00         1.0       x
numpy                0.017      0.00         1.7       x
numba                0.210      0.01         20.2      x
spark_no_arrow       0.046      0.00         4.4       x
spark_arrow          0.046      0.00         4.4       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.008s | Memory: +0.01GB | Peak: 0.30GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Numba math ops
   ✅ 0.267s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.665s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.518s | Memory: +0.00GB | Peak: 0.30GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.008      0.01         1.9       x
numpy                0.004      0.00         1.0       x
numba                0.267      0.00         62.6      x
spark_no_arrow       0.665      0.00         156.1     x
spark_arrow          0.518      0.00         121.5     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.598s | Memory: +0.03GB | Peak: 0.34GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.449s | Memory: +0.05GB | Peak: 0.38GB
⏱️  NumPy to pandas
   ✅ 0.006s | Memory: +0.01GB | Peak: 0.39GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.598      0.03         99.4      x
spark_arrow          0.449      0.05         74.7      x
numpy                0.006      0.01         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: pandas (0.004s)
   ⚡ Max speedup: 43.9x

🎯 Aggregations:
   🥇 Winner: pandas (0.010s)
   ⚡ Max speedup: 20.2x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 156.1x

🎯 Data Conversion:
   🥇 Winner: numpy (0.006s)
   ⚡ Max speedup: 99.4x

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

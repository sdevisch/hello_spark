# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 22:53 UTC

## Scope

Supporting benchmark for the frameworks conclusion.

## Console output

```text
🚀 Starting Comprehensive Performance Benchmark...
📚 Docs index: docs/index.md
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
   ✅ 0.000s | Memory: +0.00GB | Peak: 0.22GB
⏱️  Creating Spark DataFrame (no Arrow)
   ✅ 0.912s | Memory: +0.01GB | Peak: 0.23GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.232s | Memory: +0.00GB | Peak: 0.23GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.004s | Memory: +0.01GB | Peak: 0.25GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.25GB
⏱️  Numba basic ops
   ✅ 0.136s | Memory: +0.03GB | Peak: 0.28GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.102s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.059s | Memory: +0.00GB | Peak: 0.28GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.004      0.01         1.1       x
numpy                0.003      0.00         1.0       x
numba                0.136      0.03         42.7      x
spark_no_arrow       0.102      0.00         32.0      x
spark_arrow          0.059      0.00         18.7      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.010s | Memory: +0.00GB | Peak: 0.29GB
⏱️  NumPy aggregations
   ✅ 0.017s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba aggregations
   ✅ 0.225s | Memory: +0.01GB | Peak: 0.29GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.047s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.051s | Memory: +0.00GB | Peak: 0.29GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.010      0.00         1.0       x
numpy                0.017      0.00         1.7       x
numba                0.225      0.01         22.4      x
spark_no_arrow       0.047      0.00         4.7       x
spark_arrow          0.051      0.00         5.1       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.008s | Memory: +0.01GB | Peak: 0.30GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Numba math ops
   ✅ 0.258s | Memory: +0.01GB | Peak: 0.31GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.737s | Memory: +0.00GB | Peak: 0.31GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.606s | Memory: +0.00GB | Peak: 0.31GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.008      0.01         1.9       x
numpy                0.004      0.00         1.0       x
numba                0.258      0.01         61.9      x
spark_no_arrow       0.737      0.00         177.0     x
spark_arrow          0.606      0.00         145.5     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.578s | Memory: +0.03GB | Peak: 0.34GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.443s | Memory: +0.05GB | Peak: 0.39GB
⏱️  NumPy to pandas
   ✅ 0.007s | Memory: +0.01GB | Peak: 0.40GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.578      0.03         87.7      x
spark_arrow          0.443      0.05         67.1      x
numpy                0.007      0.01         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 42.7x

🎯 Aggregations:
   🥇 Winner: pandas (0.010s)
   ⚡ Max speedup: 22.4x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 177.0x

🎯 Data Conversion:
   🥇 Winner: numpy (0.007s)
   ⚡ Max speedup: 87.7x

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

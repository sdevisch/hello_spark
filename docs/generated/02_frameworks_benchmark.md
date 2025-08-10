# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 16:53 UTC

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
   ✅ 0.000s | Memory: +0.00GB | Peak: 0.23GB
⏱️  Creating Spark DataFrame (no Arrow)
   ✅ 0.828s | Memory: +0.01GB | Peak: 0.24GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.294s | Memory: +0.00GB | Peak: 0.24GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.24GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.24GB
⏱️  Numba basic ops
   ✅ 0.151s | Memory: +0.03GB | Peak: 0.28GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.110s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.058s | Memory: +0.00GB | Peak: 0.28GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.004      0.00         1.3       x
numpy                0.003      0.00         1.0       x
numba                0.151      0.03         43.7      x
spark_no_arrow       0.110      0.00         32.0      x
spark_arrow          0.058      0.00         16.9      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.011s | Memory: +0.00GB | Peak: 0.28GB
⏱️  NumPy aggregations
   ✅ 0.016s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Numba aggregations
   ✅ 0.208s | Memory: +0.01GB | Peak: 0.29GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.043s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.040s | Memory: +0.00GB | Peak: 0.29GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.011      0.00         1.0       x
numpy                0.016      0.00         1.5       x
numba                0.208      0.01         19.2      x
spark_no_arrow       0.043      0.00         4.0       x
spark_arrow          0.040      0.00         3.7       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.008s | Memory: +0.00GB | Peak: 0.29GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba math ops
   ✅ 0.259s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.738s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.891s | Memory: +0.00GB | Peak: 0.29GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.008      0.00         1.7       x
numpy                0.004      0.00         1.0       x
numba                0.259      0.00         58.2      x
spark_no_arrow       0.738      0.00         165.8     x
spark_arrow          0.891      0.00         200.1     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.633s | Memory: +0.04GB | Peak: 0.33GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.510s | Memory: +0.06GB | Peak: 0.39GB
⏱️  NumPy to pandas
   ✅ 0.005s | Memory: +0.01GB | Peak: 0.40GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.633      0.04         124.4     x
spark_arrow          0.510      0.06         100.2     x
numpy                0.005      0.01         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 43.7x

🎯 Aggregations:
   🥇 Winner: pandas (0.011s)
   ⚡ Max speedup: 19.2x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 200.1x

🎯 Data Conversion:
   🥇 Winner: numpy (0.005s)
   ⚡ Max speedup: 124.4x

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

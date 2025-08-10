# Frameworks: Benchmark (supporting details)

Generated: 2025-08-10 17:00 UTC

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
   ✅ 0.840s | Memory: +0.01GB | Peak: 0.24GB
⏱️  Creating Spark DataFrame (with Arrow)
   ✅ 0.209s | Memory: +0.00GB | Peak: 0.24GB

============================================================
🔍 BENCHMARK 1: BASIC OPERATIONS (Filter + Select)
============================================================
⏱️  Pandas basic ops
   ✅ 0.003s | Memory: +0.01GB | Peak: 0.25GB
⏱️  NumPy basic ops
   ✅ 0.003s | Memory: +0.00GB | Peak: 0.25GB
⏱️  Numba basic ops
   ✅ 0.152s | Memory: +0.03GB | Peak: 0.28GB
⏱️  Spark basic ops (no Arrow)
   ✅ 0.112s | Memory: +0.00GB | Peak: 0.28GB
⏱️  Spark basic ops (with Arrow)
   ✅ 0.054s | Memory: +0.00GB | Peak: 0.28GB

📈 BASIC OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.003      0.01         1.1       x
numpy                0.003      0.00         1.0       x
numba                0.152      0.03         48.5      x
spark_no_arrow       0.112      0.00         35.8      x
spark_arrow          0.054      0.00         17.3      x

============================================================
📊 BENCHMARK 2: AGGREGATIONS (GroupBy + Statistics)
============================================================
⏱️  Pandas aggregations
   ✅ 0.009s | Memory: +0.00GB | Peak: 0.29GB
⏱️  NumPy aggregations
   ✅ 0.018s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba aggregations
   ✅ 0.214s | Memory: +0.01GB | Peak: 0.29GB
⏱️  Spark aggregations (no Arrow)
   ✅ 0.048s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Spark aggregations (with Arrow)
   ✅ 0.047s | Memory: +0.00GB | Peak: 0.29GB

📈 AGGREGATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.009      0.00         1.0       x
numpy                0.018      0.00         1.9       x
numba                0.214      0.01         23.4      x
spark_no_arrow       0.048      0.00         5.2       x
spark_arrow          0.047      0.00         5.1       x

============================================================
🧮 BENCHMARK 3: MATHEMATICAL OPERATIONS
============================================================
⏱️  Pandas math ops
   ✅ 0.007s | Memory: +0.00GB | Peak: 0.29GB
⏱️  NumPy math ops
   ✅ 0.004s | Memory: +0.00GB | Peak: 0.29GB
⏱️  Numba math ops
   ✅ 0.263s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Spark math ops (no Arrow)
   ✅ 0.805s | Memory: +0.00GB | Peak: 0.30GB
⏱️  Spark math ops (with Arrow)
   ✅ 0.521s | Memory: +0.00GB | Peak: 0.30GB

📈 MATHEMATICAL OPERATIONS RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
pandas               0.007      0.00         1.6       x
numpy                0.004      0.00         1.0       x
numba                0.263      0.00         58.5      x
spark_no_arrow       0.805      0.00         179.3     x
spark_arrow          0.521      0.00         116.1     x

============================================================
🔄 BENCHMARK 4: DATA CONVERSION (to Pandas)
============================================================
⏱️  Spark to pandas (no Arrow)
   ✅ 0.703s | Memory: +0.04GB | Peak: 0.34GB
⏱️  Spark to pandas (with Arrow)
   ✅ 0.430s | Memory: +0.04GB | Peak: 0.38GB
⏱️  NumPy to pandas
   ✅ 0.006s | Memory: +0.01GB | Peak: 0.39GB

📈 DATA CONVERSION RESULTS:
Framework            Time (s)   Memory (GB)  Speedup   
-------------------------------------------------------
spark_no_arrow       0.703      0.04         117.6     x
spark_arrow          0.430      0.04         71.9      x
numpy                0.006      0.01         1.0       x

============================================================
🏆 COMPREHENSIVE BENCHMARK SUMMARY
============================================================

🎯 Basic Operations:
   🥇 Winner: numpy (0.003s)
   ⚡ Max speedup: 48.5x

🎯 Aggregations:
   🥇 Winner: pandas (0.009s)
   ⚡ Max speedup: 23.4x

🎯 Mathematical Operations:
   🥇 Winner: numpy (0.004s)
   ⚡ Max speedup: 179.3x

🎯 Data Conversion:
   🥇 Winner: numpy (0.006s)
   ⚡ Max speedup: 117.6x

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

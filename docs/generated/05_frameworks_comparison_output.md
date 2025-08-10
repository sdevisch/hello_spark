# Frameworks: Comprehensive comparison (Spark, pandas, NumPy, Numba)

Generated: 2025-08-10 13:59 UTC

## Console output

```text
🚀 Starting Comprehensive Framework Comparison...
💻 System: 18.0GB RAM
✅ NumPy: 2.0.2
✅ Pandas: 2.2.3
✅ Numba: 0.60.0
🔬 COMPREHENSIVE FRAMEWORK COMPARISON
============================================================
📊 Dataset size: 300,000 rows
🎯 Comparing: NumPy vs Spark.Pandas vs Pandas vs Jitted NumPy
============================================================
🔍 Attempting to enable pandas-on-spark API...
   Testing basic pandas-on-spark functionality...
✅ Spark pandas API available and functional!
   Test results: id       5
value    5
dtype: int64 rows, mean value: 6.611
🌐 Spark UI (No Arrow): http://localhost:4040
🌐 Spark UI (With Arrow): http://localhost:4041

============================================================
📊 CREATING INITIAL DATA IN SPARK
============================================================
💡 REALISTIC SCENARIO:
   - Data starts in Spark (from files, databases, etc.)
   - We'll convert to different frameworks for comparison
⏱️  Creating Spark DataFrame
   ✅ Created Spark DataFrame with 300,000 rows
   ✅ 0.4599s | Memory: +0.000GB

============================================================
🔄 CONVERTING TO DIFFERENT FRAMEWORKS
============================================================
⏱️  Spark → Pandas (with Arrow) - SERIALIZATION
   ✅ 0.3106s | Memory: +0.073GB
⏱️  Spark → Pandas (no Arrow) - EXPENSIVE SERIALIZATION
   ✅ 8.7358s | Memory: +0.071GB
⏱️  Pandas → NumPy arrays - MINIMAL SERIALIZATION
   ✅ 0.0001s | Memory: +0.000GB
⏱️  Spark → Pandas-on-Spark API - NO SERIALIZATION
   ✅ 0.0295s | Memory: +0.000GB
   ✅ Pandas-on-Spark conversion successful

📊 CONVERSION SUMMARY:
   pandas_arrow        : 0.3106s
   pandas_no_arrow     : 8.7358s
   numpy               : 0.0001s
   pandas_on_spark     : 0.0295s

============================================================
🧮 ARITHMETIC OPERATIONS COMPARISON
============================================================
⏱️  Spark arithmetic (native) - NO SERIALIZATION
   ✅ 0.0239s | Memory: +0.000GB
⏱️  Pandas arithmetic - NO SERIALIZATION (vectorized)
   ✅ 0.0042s | Memory: +0.007GB
⏱️  NumPy arithmetic - NO SERIALIZATION (pure C)
   ✅ 0.0009s | Memory: +0.007GB
⏱️  Jitted NumPy arithmetic - NO SERIALIZATION (compiled)
   ✅ 0.0010s | Memory: +0.009GB
⏱️  Pandas-on-Spark arithmetic - MINIMAL SERIALIZATION
   ✅ 0.3709s | Memory: +0.000GB
   ✅ Pandas-on-Spark arithmetic successful

📊 ARITHMETIC PERFORMANCE COMPARISON:
   spark          : 0.0239s (26.1x)
   pandas         : 0.0042s (4.6x)
   numpy          : 0.0009s (1.0x)
   numba          : 0.0010s (1.1x)
   pandas_on_spark: 0.3709s (404.0x)

============================================================
📈 AGGREGATION OPERATIONS COMPARISON
============================================================
⏱️  Spark aggregations - NO SERIALIZATION (distributed)
   ✅ 0.0251s | Memory: +0.000GB
⏱️  Pandas aggregations - NO SERIALIZATION (optimized)
   ✅ 0.0063s | Memory: +0.003GB
⏱️  NumPy aggregations - NO SERIALIZATION (manual loops)
   ✅ 0.0177s | Memory: +0.000GB
⏱️  Jitted NumPy aggregations - NO SERIALIZATION (compiled)
   ✅ 0.0158s | Memory: +0.000GB

📊 AGGREGATION PERFORMANCE COMPARISON:
   spark          : 0.0251s (4.0x)
   pandas         : 0.0063s (1.0x)
   numpy          : 0.0177s (2.8x)
   numba          : 0.0158s (2.5x)

============================================================
🔬 COMPLEX OPERATIONS - SERIALIZATION ANALYSIS
============================================================
⏱️  Spark complex ops (window, math) - NO SERIALIZATION
   ✅ 0.0255s | Memory: +0.000GB
⏱️  Pandas complex ops - NO SERIALIZATION (vectorized)
   ✅ 0.0481s | Memory: +0.015GB
⏱️  NumPy complex ops - NO SERIALIZATION (pure C)
   ✅ 0.0019s | Memory: +0.005GB

⚠️ OPERATIONS THAT CAUSE SERIALIZATION:
⏱️  Scalar extraction - SERIALIZATION (C → Python)
   ✅ 0.0000s | Memory: +0.000GB
⏱️  Array → List conversion - MASS SERIALIZATION
   ✅ 0.0000s | Memory: +0.000GB
⏱️  DataFrame → String - FULL SERIALIZATION
   ✅ 0.0045s | Memory: +0.000GB

📊 COMPLEX OPERATIONS PERFORMANCE:
   spark          : 0.0255s (13.2x)
   pandas         : 0.0481s (24.8x)
   numpy          : 0.0019s (1.0x)

============================================================
🏹 ARROW BENEFITS VS OVERHEAD ANALYSIS
============================================================
💡 ARROW ANALYSIS:
   - Arrow optimizes columnar data transfer
   - Benefits: Vectorized serialization, less memory copying
   - Overhead: Format conversion, not always zero-copy

🔍 Testing with 1,000 rows:
⏱️    No Arrow (1,000 rows)
   ✅ 0.1021s | Memory: +0.000GB
⏱️    With Arrow (1,000 rows)
   ✅ 0.0392s | Memory: +0.000GB
    Arrow speedup (Spark → pandas): 2.6x
⏱️    Spark compute (1,000 rows)
   ✅ 0.0952s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (1,000 rows)
   ✅ 0.0347s | Memory: +0.000GB
⏱️    Pandas compute (1,000 rows)
   ✅ 0.0007s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (1,000 rows)
   ✅ 0.0847s | Memory: +0.000GB
⏱️    Pandas compute (No Arrow path) (1,000 rows)
   ✅ 0.0006s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (1,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    NumPy compute (1,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Jitted NumPy compute (1,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (1,000 rows)
   ✅ 0.3249s | Memory: +0.000GB

🔍 Testing with 10,000 rows:
⏱️    No Arrow (10,000 rows)
   ✅ 0.3534s | Memory: +0.002GB
⏱️    With Arrow (10,000 rows)
   ✅ 0.0584s | Memory: +0.001GB
    Arrow speedup (Spark → pandas): 6.1x
⏱️    Spark compute (10,000 rows)
   ✅ 0.0694s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (10,000 rows)
   ✅ 0.0347s | Memory: +0.001GB
⏱️    Pandas compute (10,000 rows)
   ✅ 0.0009s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (10,000 rows)
   ✅ 0.3165s | Memory: +0.001GB
⏱️    Pandas compute (No Arrow path) (10,000 rows)
   ✅ 0.0009s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (10,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    NumPy compute (10,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    Jitted NumPy compute (10,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (10,000 rows)
   ✅ 0.3293s | Memory: +0.000GB

🔍 Testing with 50,000 rows:
⏱️    No Arrow (50,000 rows)
   ✅ 1.4261s | Memory: +0.004GB
⏱️    With Arrow (50,000 rows)
   ✅ 0.0790s | Memory: +0.003GB
    Arrow speedup (Spark → pandas): 18.1x
⏱️    Spark compute (50,000 rows)
   ✅ 0.0943s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (50,000 rows)
   ✅ 0.0520s | Memory: +0.006GB
⏱️    Pandas compute (50,000 rows)
   ✅ 0.0014s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (50,000 rows)
   ✅ 1.4182s | Memory: +0.004GB
⏱️    Pandas compute (No Arrow path) (50,000 rows)
   ✅ 0.0010s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (50,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    NumPy compute (50,000 rows)
   ✅ 0.0003s | Memory: +0.000GB
⏱️    Jitted NumPy compute (50,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (50,000 rows)
   ✅ 0.2573s | Memory: +0.000GB

🔍 Testing with 100,000 rows:
⏱️    No Arrow (100,000 rows)
   ✅ 2.7663s | Memory: +0.009GB
⏱️    With Arrow (100,000 rows)
   ✅ 0.0750s | Memory: +0.005GB
    Arrow speedup (Spark → pandas): 36.9x
⏱️    Spark compute (100,000 rows)
   ✅ 0.1438s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (100,000 rows)
   ✅ 0.0636s | Memory: +0.009GB
⏱️    Pandas compute (100,000 rows)
   ✅ 0.0013s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (100,000 rows)
   ✅ 2.7345s | Memory: +0.012GB
⏱️    Pandas compute (No Arrow path) (100,000 rows)
   ✅ 0.0014s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (100,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    NumPy compute (100,000 rows)
   ✅ 0.0007s | Memory: +0.000GB
⏱️    Jitted NumPy compute (100,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (100,000 rows)
   ✅ 0.2884s | Memory: +0.000GB

📊 ARROW SCALING ANALYSIS:
    1,000 rows:
      Spark→pandas Arrow speedup:  2.6x
      Compute spark          : 0.0952s
      Compute pandas         : 0.0007s
      Compute numpy          : 0.0000s
      Compute numba          : 0.0000s
      Compute pandas_on_spark: 0.3249s
      Total pandas (Arrow): 0.0399s
      Total pandas (NoArrow): 0.1026s
      Total NumPy (Arrow):  0.0392s
      Total NumPy (NoArrow):0.1021s
      Total Numba (Arrow):  0.0392s
      Total Numba (NoArrow):0.1021s
   10,000 rows:
      Spark→pandas Arrow speedup:  6.1x
      Compute spark          : 0.0694s
      Compute pandas         : 0.0009s
      Compute numpy          : 0.0001s
      Compute numba          : 0.0000s
      Compute pandas_on_spark: 0.3293s
      Total pandas (Arrow): 0.0593s
      Total pandas (NoArrow): 0.3543s
      Total NumPy (Arrow):  0.0584s
      Total NumPy (NoArrow):0.3534s
      Total Numba (Arrow):  0.0584s
      Total Numba (NoArrow):0.3534s
   50,000 rows:
      Spark→pandas Arrow speedup: 18.1x
      Compute spark          : 0.0943s
      Compute pandas         : 0.0014s
      Compute numpy          : 0.0003s
      Compute numba          : 0.0000s
      Compute pandas_on_spark: 0.2573s
      Total pandas (Arrow): 0.0804s
      Total pandas (NoArrow): 1.4271s
      Total NumPy (Arrow):  0.0792s
      Total NumPy (NoArrow):1.4263s
      Total Numba (Arrow):  0.0790s
      Total Numba (NoArrow):1.4261s
   100,000 rows:
      Spark→pandas Arrow speedup: 36.9x
      Compute spark          : 0.1438s
      Compute pandas         : 0.0013s
      Compute numpy          : 0.0007s
      Compute numba          : 0.0001s
      Compute pandas_on_spark: 0.2884s
      Total pandas (Arrow): 0.0763s
      Total pandas (NoArrow): 2.7678s
      Total NumPy (Arrow):  0.0757s
      Total NumPy (NoArrow):2.7671s
      Total Numba (Arrow):  0.0751s
      Total Numba (NoArrow):2.7664s

============================================================
🏆 COMPREHENSIVE FRAMEWORK COMPARISON SUMMARY
============================================================

🎯 KEY FINDINGS:

⚡ PERFORMANCE HIERARCHY (typical):
   1. Jitted NumPy (Numba)   - Fastest computation
   2. NumPy (vectorized)     - Fast C operations
   3. Pandas (vectorized)    - Optimized single-machine
   4. Spark (distributed)    - Scales to large data
   5. Pandas-on-Spark        - Convenient but overhead

🔄 SERIALIZATION COSTS:
   Conversion times from Spark:
     pandas_arrow        : 0.3106s
     pandas_no_arrow     : 8.7358s
     numpy               : 0.0001s
     pandas_on_spark     : 0.0295s

🏹 ARROW BENEFITS:
   Average Arrow speedup: 15.9x
   • Most beneficial for: Large datasets, wide tables
   • Less beneficial for: Small datasets, simple operations

💡 DECISION FRAMEWORK:

✅ USE NUMPY WHEN:
   • Single-machine data fits in memory
   • Heavy mathematical computations
   • Maximum performance for numerical operations
   • Simple data structures (arrays)

✅ USE PANDAS WHEN:
   • Single-machine data with complex structure
   • Data manipulation and cleaning
   • Integration with existing pandas ecosystem
   • Time series and statistical analysis

✅ USE SPARK WHEN:
   • Data too large for single machine
   • Distributed computing required
   • Integration with big data ecosystem
   • Fault tolerance and scalability needed

✅ USE JITTED NUMPY (NUMBA) WHEN:
   • Custom algorithms not vectorizable
   • Complex loops and conditionals
   • Maximum performance for specialized operations
   • Can amortize JIT compilation cost

✅ USE ARROW WHEN:
   • Converting between Spark and pandas
   • Large datasets with columnar operations
   • Cross-language data exchange
   • Memory efficiency is critical

⚠️ SERIALIZATION HOTSPOTS TO AVOID:
   • Frequent scalar extraction from arrays
   • Unnecessary .tolist() conversions
   • Mixing frameworks in tight loops
   • String representations of large arrays

🎯 GOLDEN RULES:
   1. 'Right tool for the right job'
   2. 'Stay within one framework as long as possible'
   3. 'Measure before optimizing'
   4. 'Consider total cost: computation + conversion'
   5. 'Use Arrow for Spark ↔ pandas conversions'

🧹 Cleaning up...
   ✅ Stopped Spark sessions

👋 Framework comparison completed!
```

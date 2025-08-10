# Frameworks: Comprehensive comparison (Spark, pandas, NumPy, Numba)

Generated: 2025-08-10 15:13 UTC

## Console output

```text
🚀 Starting Comprehensive Framework Comparison...
💻 System: 18.0GB RAM
✅ NumPy: 2.1.3
✅ Pandas: 2.3.1
✅ Numba: 0.61.2
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
dtype: int64 rows, mean value: 4.334
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
   ✅ 0.4606s | Memory: +0.000GB

============================================================
🔄 CONVERTING TO DIFFERENT FRAMEWORKS
============================================================
⏱️  Spark → Pandas (with Arrow) - SERIALIZATION
   ✅ 0.3465s | Memory: +0.072GB
⏱️  Spark → Pandas (no Arrow) - EXPENSIVE SERIALIZATION
   ✅ 6.4946s | Memory: +0.080GB
⏱️  Pandas → NumPy arrays - MINIMAL SERIALIZATION
   ✅ 0.0001s | Memory: +0.000GB
⏱️  Spark → Pandas-on-Spark API - NO SERIALIZATION
   ✅ 0.0272s | Memory: +0.000GB
   ✅ Pandas-on-Spark conversion successful

📊 CONVERSION SUMMARY:
   pandas_arrow        : 0.3465s
   pandas_no_arrow     : 6.4946s
   numpy               : 0.0001s
   pandas_on_spark     : 0.0272s

============================================================
🧮 ARITHMETIC OPERATIONS COMPARISON
============================================================
⏱️  Spark arithmetic (native) - NO SERIALIZATION
   ✅ 0.0125s | Memory: +0.000GB
⏱️  Pandas arithmetic - NO SERIALIZATION (vectorized)
   ✅ 0.0044s | Memory: +0.013GB
⏱️  NumPy arithmetic - NO SERIALIZATION (pure C)
   ✅ 0.0009s | Memory: +0.007GB
⏱️  Jitted NumPy arithmetic - NO SERIALIZATION (compiled)
   ✅ 0.0009s | Memory: +0.009GB
⏱️  Pandas-on-Spark arithmetic - MINIMAL SERIALIZATION
   ✅ 0.3550s | Memory: +0.000GB
   ✅ Pandas-on-Spark arithmetic successful

📊 ARITHMETIC PERFORMANCE COMPARISON:
   spark          : 0.0125s (13.8x)
   pandas         : 0.0044s (4.8x)
   numpy          : 0.0009s (1.0x)
   numba          : 0.0009s (1.0x)
   pandas_on_spark: 0.3550s (392.8x)

============================================================
📈 AGGREGATION OPERATIONS COMPARISON
============================================================
⏱️  Spark aggregations - NO SERIALIZATION (distributed)
   ✅ 0.0206s | Memory: +0.000GB
⏱️  Pandas aggregations - NO SERIALIZATION (optimized)
   ✅ 0.0050s | Memory: +0.000GB
⏱️  NumPy aggregations - NO SERIALIZATION (manual loops)
   ✅ 0.0168s | Memory: +0.000GB
⏱️  Jitted NumPy aggregations - NO SERIALIZATION (compiled)
   ✅ 0.0163s | Memory: +0.000GB

📊 AGGREGATION PERFORMANCE COMPARISON:
   spark          : 0.0206s (4.1x)
   pandas         : 0.0050s (1.0x)
   numpy          : 0.0168s (3.3x)
   numba          : 0.0163s (3.2x)

============================================================
🔬 COMPLEX OPERATIONS - SERIALIZATION ANALYSIS
============================================================
⏱️  Spark complex ops (window, math) - NO SERIALIZATION
   ✅ 0.0252s | Memory: +0.000GB
⏱️  Pandas complex ops - NO SERIALIZATION (vectorized)
   ✅ 0.0493s | Memory: +0.031GB
⏱️  NumPy complex ops - NO SERIALIZATION (pure C)
   ✅ 0.0021s | Memory: +0.007GB

⚠️ OPERATIONS THAT CAUSE SERIALIZATION:
⏱️  Scalar extraction - SERIALIZATION (C → Python)
   ✅ 0.0000s | Memory: +0.000GB
⏱️  Array → List conversion - MASS SERIALIZATION
   ✅ 0.0000s | Memory: +0.000GB
⏱️  DataFrame → String - FULL SERIALIZATION
   ✅ 0.0034s | Memory: +0.000GB

📊 COMPLEX OPERATIONS PERFORMANCE:
   spark          : 0.0252s (11.9x)
   pandas         : 0.0493s (23.3x)
   numpy          : 0.0021s (1.0x)

============================================================
🏹 ARROW BENEFITS VS OVERHEAD ANALYSIS
============================================================
💡 ARROW ANALYSIS:
   - Arrow optimizes columnar data transfer
   - Benefits: Vectorized serialization, less memory copying
   - Overhead: Format conversion, not always zero-copy

🔍 Testing with 1,000 rows:
⏱️    No Arrow (1,000 rows)
   ✅ 0.1547s | Memory: +0.001GB
⏱️    With Arrow (1,000 rows)
   ✅ 0.0612s | Memory: +0.000GB
    Arrow speedup (Spark → pandas): 2.5x
⏱️    Spark compute (1,000 rows)
   ✅ 0.0689s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (1,000 rows)
   ✅ 0.0300s | Memory: +0.000GB
⏱️    Pandas compute (1,000 rows)
   ✅ 0.0006s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (1,000 rows)
   ✅ 0.1325s | Memory: +0.000GB
⏱️    Pandas compute (No Arrow path) (1,000 rows)
   ✅ 0.0005s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (1,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    NumPy compute (1,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Jitted NumPy compute (1,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (1,000 rows)
   ✅ 0.3282s | Memory: +0.000GB

🔍 Testing with 10,000 rows:
⏱️    No Arrow (10,000 rows)
   ✅ 0.3707s | Memory: +0.003GB
⏱️    With Arrow (10,000 rows)
   ✅ 0.0341s | Memory: +0.001GB
    Arrow speedup (Spark → pandas): 10.9x
⏱️    Spark compute (10,000 rows)
   ✅ 0.0620s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (10,000 rows)
   ✅ 0.0312s | Memory: +0.001GB
⏱️    Pandas compute (10,000 rows)
   ✅ 0.0005s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (10,000 rows)
   ✅ 0.3272s | Memory: +0.001GB
⏱️    Pandas compute (No Arrow path) (10,000 rows)
   ✅ 0.0009s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (10,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    NumPy compute (10,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Jitted NumPy compute (10,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (10,000 rows)
   ✅ 0.2798s | Memory: +0.000GB

🔍 Testing with 50,000 rows:
⏱️    No Arrow (50,000 rows)
   ✅ 1.0768s | Memory: +0.006GB
⏱️    With Arrow (50,000 rows)
   ✅ 0.0520s | Memory: +0.003GB
    Arrow speedup (Spark → pandas): 20.7x
⏱️    Spark compute (50,000 rows)
   ✅ 0.1203s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (50,000 rows)
   ✅ 0.0635s | Memory: +0.003GB
⏱️    Pandas compute (50,000 rows)
   ✅ 0.0008s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (50,000 rows)
   ✅ 1.1577s | Memory: +0.008GB
⏱️    Pandas compute (No Arrow path) (50,000 rows)
   ✅ 0.0007s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (50,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    NumPy compute (50,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    Jitted NumPy compute (50,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (50,000 rows)
   ✅ 0.3720s | Memory: +0.000GB

🔍 Testing with 100,000 rows:
⏱️    No Arrow (100,000 rows)
   ✅ 2.0155s | Memory: +0.011GB
⏱️    With Arrow (100,000 rows)
   ✅ 0.0654s | Memory: +0.005GB
    Arrow speedup (Spark → pandas): 30.8x
⏱️    Spark compute (100,000 rows)
   ✅ 0.0718s | Memory: +0.000GB
⏱️    Convert (Arrow) pandas ready (100,000 rows)
   ✅ 0.0725s | Memory: +0.005GB
⏱️    Pandas compute (100,000 rows)
   ✅ 0.0015s | Memory: +0.000GB
⏱️    Convert (No Arrow) pandas ready (100,000 rows)
   ✅ 1.9686s | Memory: +0.013GB
⏱️    Pandas compute (No Arrow path) (100,000 rows)
   ✅ 0.0014s | Memory: +0.000GB
⏱️    Prepare NumPy arrays (100,000 rows)
   ✅ 0.0000s | Memory: +0.000GB
⏱️    NumPy compute (100,000 rows)
   ✅ 0.0007s | Memory: +0.000GB
⏱️    Jitted NumPy compute (100,000 rows)
   ✅ 0.0001s | Memory: +0.000GB
⏱️    Pandas-on-Spark compute (100,000 rows)
   ✅ 0.2778s | Memory: +0.000GB

📊 ARROW SCALING ANALYSIS:
    1,000 rows:
      Spark→pandas Arrow speedup:  2.5x
      Compute spark          : 0.0689s
      Compute pandas         : 0.0006s
      Compute numpy          : 0.0000s
      Compute numba          : 0.0000s
      Compute pandas_on_spark: 0.3282s
      Total pandas (Arrow): 0.0617s
      Total pandas (NoArrow): 0.1553s
      Total NumPy (Arrow):  0.0612s
      Total NumPy (NoArrow):0.1548s
      Total Numba (Arrow):  0.0612s
      Total Numba (NoArrow):0.1547s
   10,000 rows:
      Spark→pandas Arrow speedup: 10.9x
      Compute spark          : 0.0620s
      Compute pandas         : 0.0005s
      Compute numpy          : 0.0000s
      Compute numba          : 0.0000s
      Compute pandas_on_spark: 0.2798s
      Total pandas (Arrow): 0.0346s
      Total pandas (NoArrow): 0.3716s
      Total NumPy (Arrow):  0.0341s
      Total NumPy (NoArrow):0.3708s
      Total Numba (Arrow):  0.0341s
      Total Numba (NoArrow):0.3707s
   50,000 rows:
      Spark→pandas Arrow speedup: 20.7x
      Compute spark          : 0.1203s
      Compute pandas         : 0.0008s
      Compute numpy          : 0.0001s
      Compute numba          : 0.0001s
      Compute pandas_on_spark: 0.3720s
      Total pandas (Arrow): 0.0528s
      Total pandas (NoArrow): 1.0775s
      Total NumPy (Arrow):  0.0521s
      Total NumPy (NoArrow):1.0769s
      Total Numba (Arrow):  0.0521s
      Total Numba (NoArrow):1.0769s
   100,000 rows:
      Spark→pandas Arrow speedup: 30.8x
      Compute spark          : 0.0718s
      Compute pandas         : 0.0015s
      Compute numpy          : 0.0007s
      Compute numba          : 0.0001s
      Compute pandas_on_spark: 0.2778s
      Total pandas (Arrow): 0.0669s
      Total pandas (NoArrow): 2.0169s
      Total NumPy (Arrow):  0.0661s
      Total NumPy (NoArrow):2.0162s
      Total Numba (Arrow):  0.0655s
      Total Numba (NoArrow):2.0156s

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
     pandas_arrow        : 0.3465s
     pandas_no_arrow     : 6.4946s
     numpy               : 0.0001s
     pandas_on_spark     : 0.0272s

🏹 ARROW BENEFITS:
   Average Arrow speedup: 16.2x
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

#!/usr/bin/env python3
"""
Comprehensive Framework Comparison: Start with the conclusion
=============================================================

Main conclusion (last-page-first):
- In a Spark context, first preference is: stay in Spark with native functions. When moving to a single machine, use Arrow to convert to pandas and keep operations vectorized in pandas.
- Only use NumPy / jitted NumPy (Numba) for targeted kernels that pandas cannot express efficiently. Those are niche and isolated.

This script demonstrates a realistic scenario comparing four frameworks:
1. Spark (native) and pandas API on Spark
2. Pandas (Arrow vs no Arrow conversions)
3. NumPy (vectorized C operations)
4. Jitted NumPy with Numba (specialized kernels)

Focus Areas:
- Common data operations across frameworks
- Where serialization occurs and the impact
- Arrow benefits vs overhead
- JIT compilation advantages and costs
- Decision framework for choosing the right tool

Scenario: Data starts in Spark; we compare staying in Spark vs converting.
"""

import time
import numpy as np
import pandas as pd
import psutil
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col

# Handle NumPy 2.0 compatibility for pandas-on-spark
def fix_numpy_compatibility():
    """Fix NumPy 2.0 compatibility issues with pandas-on-spark"""
    # Set Arrow environment variable first
    os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'
    
    # Fix multiple NumPy 2.0 compatibility issues
    compatibility_fixes = {
        'NaN': 'nan',
        'string_': 'bytes_',
        'unicode_': 'str_',
        'int_': 'int64',
        'float_': 'float64',
        'complex_': 'complex128',
        'bool_': 'bool',
    }
    
    for old_attr, new_attr in compatibility_fixes.items():
        if not hasattr(np, old_attr) and hasattr(np, new_attr):
            setattr(np, old_attr, getattr(np, new_attr))

fix_numpy_compatibility()

try:
    import numba
    from numba import jit, njit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    print("⚠️ Numba not available - JIT examples will be skipped")

class FrameworkComparison:
    def __init__(self, rows=200_000):
        """Initialize comparison with multiple frameworks"""
        self.rows = rows
        
        print("🔬 COMPREHENSIVE FRAMEWORK COMPARISON")
        print("=" * 60)
        print(f"📊 Dataset size: {rows:,} rows")
        print("🎯 Comparing: NumPy vs Spark.Pandas vs Pandas vs Jitted NumPy")
        print("=" * 60)
        
        # Initialize Spark sessions
        self.spark_no_arrow = SparkSession.builder \
            .appName("Framework-Comparison-NoArrow") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .config("spark.sql.adaptive.enabled", "false") \
            .getOrCreate()
        
        self.spark_with_arrow = SparkSession.builder \
            .appName("Framework-Comparison-WithArrow") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.sql.adaptive.enabled", "false") \
            .getOrCreate()
        
        # Enable pandas API on Spark (Spark 3.2+)
        # Fix NumPy 2.0 compatibility issue  
        self.pandas_on_spark_available = False
        print("🔍 Attempting to enable pandas-on-spark API...")
        
        try:
            # Re-apply compatibility fixes just before import
            fix_numpy_compatibility()
            
            import pyspark.pandas as ps
            
            # Test basic functionality with a small DataFrame
            print("   Testing basic pandas-on-spark functionality...")
            test_df = self.spark_with_arrow.range(5).select(
                col("id"),
                (F.rand() * 10).alias("value")
            )
            test_ps = ps.DataFrame(test_df)
            
            # Test multiple operations to ensure compatibility
            count = test_ps.count()
            mean_val = test_ps['value'].mean()
            
            self.pandas_on_spark_available = True
            print("✅ Spark pandas API available and functional!")
            print(f"   Test results: {count} rows, mean value: {mean_val:.3f}")
            
        except Exception as e:
            self.pandas_on_spark_available = False
            error_str = str(e)
            print(f"⚠️ Spark pandas API not available: {error_str[:100]}...")
            
            if any(term in error_str for term in ["NaN", "string_", "unicode_", "numpy"]):
                print("   🔧 NumPy 2.0 compatibility issue detected")
                print("   💡 Recommendations:")
                print("      - Downgrade NumPy: pip install 'numpy<2.0'") 
                print("      - Or upgrade PySpark when compatible version available")
            else:
                print("   This may be due to PySpark version or environment issues")
        
        self.spark_no_arrow.sparkContext.setLogLevel("WARN")
        self.spark_with_arrow.sparkContext.setLogLevel("WARN")
        
        print(f"🌐 Spark UI (No Arrow): http://localhost:4040")
        print(f"🌐 Spark UI (With Arrow): http://localhost:4041")

    def get_memory_usage(self):
        """Get current memory usage in GB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024**3)

    def time_operation(self, name, func, *args, **kwargs):
        """Time an operation with memory tracking"""
        start_memory = self.get_memory_usage()
        print(f"⏱️  {name}")
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        end_memory = self.get_memory_usage()
        duration = end_time - start_time
        memory_delta = end_memory - start_memory
        
        print(f"   ✅ {duration:.4f}s | Memory: {memory_delta:+.3f}GB")
        return result, duration

    def create_initial_data(self):
        """Create initial data in Spark - realistic starting point"""
        print("\n" + "="*60)
        print("📊 CREATING INITIAL DATA IN SPARK")
        print("="*60)
        
        print("💡 REALISTIC SCENARIO:")
        print("   - Data starts in Spark (from files, databases, etc.)")
        print("   - We'll convert to different frameworks for comparison")
        
        def create_spark_data():
            # Create comprehensive dataset in Spark
            spark_df = self.spark_with_arrow.range(self.rows).select(
                col("id"),
                # Numerical data for computations
                (F.rand() * 100).alias("values"),
                (F.rand() * 50 + 25).alias("prices"),
                (F.rand() * 1000).alias("quantities"),
                
                # Categorical data
                (F.rand() * 5).cast("int").alias("category"),
                (F.rand() > 0.7).alias("is_premium"),
                
                # Date/time simulation
                (F.rand() * 365).cast("int").alias("days_offset"),
                
                # Complex calculations
                ((F.rand() * 100) * (F.rand() * 50 + 25)).alias("revenue"),
                (F.rand() * 20 - 10).alias("profit_margin")
            ).cache()
            
            # Force materialization
            count = spark_df.count()
            print(f"   ✅ Created Spark DataFrame with {count:,} rows")
            
            return spark_df
        
        spark_df, creation_time = self.time_operation("Creating Spark DataFrame", create_spark_data)
        
        return spark_df

    def convert_to_frameworks(self, spark_df):
        """Convert Spark data to all other frameworks"""
        print("\n" + "="*60)
        print("🔄 CONVERTING TO DIFFERENT FRAMEWORKS")
        print("="*60)
        
        conversions = {}
        
        # 1. Convert to pandas (with Arrow)
        def to_pandas_arrow():
            return spark_df.toPandas()
        
        pandas_df, pandas_time = self.time_operation(
            "Spark → Pandas (with Arrow) - SERIALIZATION", 
            to_pandas_arrow
        )
        conversions['pandas_arrow'] = (pandas_df, pandas_time)
        
        # 2. Convert to pandas (without Arrow)
        def to_pandas_no_arrow():
            return self.spark_no_arrow.createDataFrame(
                spark_df.collect()  # This forces expensive serialization
            ).toPandas()
        
        pandas_df_no_arrow, pandas_no_arrow_time = self.time_operation(
            "Spark → Pandas (no Arrow) - EXPENSIVE SERIALIZATION",
            to_pandas_no_arrow
        )
        conversions['pandas_no_arrow'] = (pandas_df_no_arrow, pandas_no_arrow_time)
        
        # 3. Convert to NumPy arrays
        def to_numpy():
            pdf = pandas_df  # Use already converted pandas
            return {
                'values': pdf['values'].values,
                'prices': pdf['prices'].values,
                'quantities': pdf['quantities'].values,
                'revenue': pdf['revenue'].values,
                'profit_margin': pdf['profit_margin'].values,
                'category': pdf['category'].values,
                'is_premium': pdf['is_premium'].values
            }
        
        numpy_arrays, numpy_time = self.time_operation(
            "Pandas → NumPy arrays - MINIMAL SERIALIZATION",
            to_numpy
        )
        conversions['numpy'] = (numpy_arrays, numpy_time)
        
        # 4. Pandas on Spark (if available)
        if self.pandas_on_spark_available:
            try:
                def to_pandas_on_spark():
                    import pyspark.pandas as ps
                    # Create pandas-on-spark DataFrame from Spark DataFrame
                    return ps.DataFrame(spark_df)
                
                ps_df, ps_time = self.time_operation(
                    "Spark → Pandas-on-Spark API - NO SERIALIZATION",
                    to_pandas_on_spark
                )
                conversions['pandas_on_spark'] = (ps_df, ps_time)
                print("   ✅ Pandas-on-Spark conversion successful")
                
            except Exception as e:
                print(f"   ⚠️ Pandas-on-Spark conversion failed: {e}")
                # Don't disable globally, just skip this conversion
                print("   Continuing without pandas-on-spark in comparisons...")
        
        print(f"\n📊 CONVERSION SUMMARY:")
        for name, (_, time_taken) in conversions.items():
            print(f"   {name:20}: {time_taken:.4f}s")
        
        return conversions

    def demo_arithmetic_operations(self, spark_df, conversions):
        """Compare arithmetic operations across frameworks"""
        print("\n" + "="*60)
        print("🧮 ARITHMETIC OPERATIONS COMPARISON")
        print("="*60)
        
        results = {}
        
        # 1. Spark DataFrame operations (no serialization)
        def spark_arithmetic():
            return spark_df.select(
                col("id"),
                (col("values") * col("prices")).alias("total_value"),
                (col("revenue") * (1 + col("profit_margin") / 100)).alias("adjusted_revenue"),
                F.sqrt(col("values")).alias("sqrt_values"),
                (col("quantities") + col("values") * 2).alias("weighted_qty")
            )
        
        spark_result, spark_time = self.time_operation(
            "Spark arithmetic (native) - NO SERIALIZATION",
            spark_arithmetic
        )
        results['spark'] = spark_time
        
        # 2. Pandas operations
        if 'pandas_arrow' in conversions:
            pandas_df, _ = conversions['pandas_arrow']
            
            def pandas_arithmetic():
                result_df = pandas_df.copy()
                result_df['total_value'] = result_df['values'] * result_df['prices']
                result_df['adjusted_revenue'] = result_df['revenue'] * (1 + result_df['profit_margin'] / 100)
                result_df['sqrt_values'] = np.sqrt(result_df['values'])
                result_df['weighted_qty'] = result_df['quantities'] + result_df['values'] * 2
                return result_df
            
            pandas_result, pandas_time = self.time_operation(
                "Pandas arithmetic - NO SERIALIZATION (vectorized)",
                pandas_arithmetic
            )
            results['pandas'] = pandas_time
        
        # 3. NumPy operations
        if 'numpy' in conversions:
            numpy_arrays, _ = conversions['numpy']
            
            def numpy_arithmetic():
                return {
                    'total_value': numpy_arrays['values'] * numpy_arrays['prices'],
                    'adjusted_revenue': numpy_arrays['revenue'] * (1 + numpy_arrays['profit_margin'] / 100),
                    'sqrt_values': np.sqrt(numpy_arrays['values']),
                    'weighted_qty': numpy_arrays['quantities'] + numpy_arrays['values'] * 2
                }
            
            numpy_result, numpy_time = self.time_operation(
                "NumPy arithmetic - NO SERIALIZATION (pure C)",
                numpy_arithmetic
            )
            results['numpy'] = numpy_time
        
        # 4. Jitted NumPy (if available)
        if NUMBA_AVAILABLE and 'numpy' in conversions:
            @njit  # No-python mode for maximum performance
            def jitted_arithmetic(values, prices, revenue, profit_margin, quantities):
                n = len(values)
                total_value = np.empty(n)
                adjusted_revenue = np.empty(n)
                sqrt_values = np.empty(n)
                weighted_qty = np.empty(n)
                
                for i in range(n):
                    total_value[i] = values[i] * prices[i]
                    adjusted_revenue[i] = revenue[i] * (1 + profit_margin[i] / 100)
                    sqrt_values[i] = np.sqrt(values[i])
                    weighted_qty[i] = quantities[i] + values[i] * 2
                
                return total_value, adjusted_revenue, sqrt_values, weighted_qty
            
            # Warmup JIT compilation
            small_arrays = {k: v[:100] for k, v in numpy_arrays.items()}
            _ = jitted_arithmetic(
                small_arrays['values'], small_arrays['prices'], 
                small_arrays['revenue'], small_arrays['profit_margin'], 
                small_arrays['quantities']
            )
            
            def numba_arithmetic():
                return jitted_arithmetic(
                    numpy_arrays['values'], numpy_arrays['prices'],
                    numpy_arrays['revenue'], numpy_arrays['profit_margin'],
                    numpy_arrays['quantities']
                )
            
            numba_result, numba_time = self.time_operation(
                "Jitted NumPy arithmetic - NO SERIALIZATION (compiled)",
                numba_arithmetic
            )
            results['numba'] = numba_time
        
        # 5. Pandas on Spark (if available)
        if self.pandas_on_spark_available and 'pandas_on_spark' in conversions:
            try:
                ps_df, _ = conversions['pandas_on_spark']
                
                def pandas_on_spark_arithmetic():
                    # Create new columns using pandas-on-spark syntax
                    # This leverages Spark's distributed computing while providing pandas-like API
                    import pyspark.pandas as ps
                    
                    result_df = ps_df.assign(
                        total_value=ps_df['values'] * ps_df['prices'],
                        adjusted_revenue=ps_df['revenue'] * (1 + ps_df['profit_margin'] / 100),
                        sqrt_values=ps_df['values'] ** 0.5,  # Avoid numpy functions
                        weighted_qty=ps_df['quantities'] + ps_df['values'] * 2
                    )
                    
                    # Force computation by accessing result
                    _ = result_df.count()
                    return result_df
                
                ps_result, ps_time = self.time_operation(
                    "Pandas-on-Spark arithmetic - MINIMAL SERIALIZATION",
                    pandas_on_spark_arithmetic
                )
                results['pandas_on_spark'] = ps_time
                print("   ✅ Pandas-on-Spark arithmetic successful")
                
            except Exception as e:
                print(f"   ⚠️ Pandas-on-Spark arithmetic failed: {e}")
                print("   This may be due to API differences or compatibility issues")
        
        print(f"\n📊 ARITHMETIC PERFORMANCE COMPARISON:")
        if results:
            fastest_time = min(results.values())
            for framework, time_taken in results.items():
                speedup = time_taken / fastest_time
                print(f"   {framework:15}: {time_taken:.4f}s ({speedup:.1f}x)")
        
        return results

    def demo_aggregation_operations(self, spark_df, conversions):
        """Compare aggregation operations across frameworks"""
        print("\n" + "="*60)
        print("📈 AGGREGATION OPERATIONS COMPARISON")
        print("="*60)
        
        results = {}
        
        # 1. Spark aggregations
        def spark_aggregations():
            return spark_df.groupBy("category").agg(
                F.avg("values").alias("avg_values"),
                F.sum("revenue").alias("total_revenue"),
                F.stddev("prices").alias("std_prices"),
                F.count("*").alias("count"),
                F.max("quantities").alias("max_qty")
            )
        
        spark_agg, spark_time = self.time_operation(
            "Spark aggregations - NO SERIALIZATION (distributed)",
            spark_aggregations
        )
        results['spark'] = spark_time
        
        # 2. Pandas aggregations
        if 'pandas_arrow' in conversions:
            pandas_df, _ = conversions['pandas_arrow']
            
            def pandas_aggregations():
                return pandas_df.groupby('category').agg({
                    'values': 'mean',
                    'revenue': 'sum',
                    'prices': 'std',
                    'id': 'count',
                    'quantities': 'max'
                })
            
            pandas_agg, pandas_time = self.time_operation(
                "Pandas aggregations - NO SERIALIZATION (optimized)",
                pandas_aggregations
            )
            results['pandas'] = pandas_time
        
        # 3. NumPy aggregations (manual grouping)
        if 'numpy' in conversions:
            numpy_arrays, _ = conversions['numpy']
            
            def numpy_aggregations():
                categories = numpy_arrays['category']
                unique_cats = np.unique(categories)
                
                results_dict = {}
                for cat in unique_cats:
                    mask = categories == cat
                    results_dict[cat] = {
                        'avg_values': np.mean(numpy_arrays['values'][mask]),
                        'total_revenue': np.sum(numpy_arrays['revenue'][mask]),
                        'std_prices': np.std(numpy_arrays['prices'][mask]),
                        'count': np.sum(mask),
                        'max_qty': np.max(numpy_arrays['quantities'][mask])
                    }
                return results_dict
            
            numpy_agg, numpy_time = self.time_operation(
                "NumPy aggregations - NO SERIALIZATION (manual loops)",
                numpy_aggregations
            )
            results['numpy'] = numpy_time
        
        # 4. Jitted NumPy aggregations
        if NUMBA_AVAILABLE and 'numpy' in conversions:
            @njit
            def jitted_group_agg(categories, values, revenue, prices, quantities):
                unique_cats = np.unique(categories)
                n_cats = len(unique_cats)
                
                avg_values = np.empty(n_cats)
                total_revenue = np.empty(n_cats)
                std_prices = np.empty(n_cats)
                counts = np.empty(n_cats, dtype=np.int64)
                max_qty = np.empty(n_cats)
                
                for i, cat in enumerate(unique_cats):
                    mask = categories == cat
                    avg_values[i] = np.mean(values[mask])
                    total_revenue[i] = np.sum(revenue[mask])
                    std_prices[i] = np.std(prices[mask])
                    counts[i] = np.sum(mask)
                    max_qty[i] = np.max(quantities[mask])
                
                return avg_values, total_revenue, std_prices, counts, max_qty
            
            # Warmup
            small_arrays = {k: v[:100] for k, v in numpy_arrays.items()}
            _ = jitted_group_agg(
                small_arrays['category'], small_arrays['values'],
                small_arrays['revenue'], small_arrays['prices'], 
                small_arrays['quantities']
            )
            
            def numba_aggregations():
                return jitted_group_agg(
                    numpy_arrays['category'], numpy_arrays['values'],
                    numpy_arrays['revenue'], numpy_arrays['prices'],
                    numpy_arrays['quantities']
                )
            
            numba_agg, numba_time = self.time_operation(
                "Jitted NumPy aggregations - NO SERIALIZATION (compiled)",
                numba_aggregations
            )
            results['numba'] = numba_time
        
        print(f"\n📊 AGGREGATION PERFORMANCE COMPARISON:")
        if results:
            fastest_time = min(results.values())
            for framework, time_taken in results.items():
                speedup = time_taken / fastest_time
                print(f"   {framework:15}: {time_taken:.4f}s ({speedup:.1f}x)")
        
        return results

    def demo_complex_operations(self, spark_df, conversions):
        """Compare complex operations that may trigger serialization"""
        print("\n" + "="*60)
        print("🔬 COMPLEX OPERATIONS - SERIALIZATION ANALYSIS")
        print("="*60)
        
        results = {}
        
        # 1. Complex Spark operations
        def spark_complex():
            # Window functions and complex expressions
            from pyspark.sql.window import Window
            
            window = Window.partitionBy("category").orderBy("values")
            
            return spark_df.select(
                col("id"),
                col("category"),
                col("values"),
                # Complex mathematical operations
                F.exp(col("values") / 100).alias("exp_values"),
                F.log(col("values") + 1).alias("log_values"),
                # Window functions
                F.row_number().over(window).alias("row_num"),
                F.lag("values").over(window).alias("prev_values"),
                # Conditional operations
                F.when(col("is_premium"), col("prices") * 1.2)
                 .otherwise(col("prices")).alias("adjusted_prices")
            )
        
        spark_complex_result, spark_time = self.time_operation(
            "Spark complex ops (window, math) - NO SERIALIZATION",
            spark_complex
        )
        results['spark'] = spark_time
        
        # 2. Pandas complex operations
        if 'pandas_arrow' in conversions:
            pandas_df, _ = conversions['pandas_arrow']
            
            def pandas_complex():
                result_df = pandas_df.copy()
                
                # Mathematical operations
                result_df['exp_values'] = np.exp(result_df['values'] / 100)
                result_df['log_values'] = np.log(result_df['values'] + 1)
                
                # Window-like operations
                result_df['row_num'] = result_df.groupby('category')['values'].rank()
                result_df['prev_values'] = result_df.groupby('category')['values'].shift(1)
                
                # Conditional operations
                result_df['adjusted_prices'] = np.where(
                    result_df['is_premium'], 
                    result_df['prices'] * 1.2, 
                    result_df['prices']
                )
                
                return result_df
            
            pandas_complex_result, pandas_time = self.time_operation(
                "Pandas complex ops - NO SERIALIZATION (vectorized)",
                pandas_complex
            )
            results['pandas'] = pandas_time
        
        # 3. NumPy complex operations
        if 'numpy' in conversions:
            numpy_arrays, _ = conversions['numpy']
            
            def numpy_complex():
                values = numpy_arrays['values']
                prices = numpy_arrays['prices']
                is_premium = numpy_arrays['is_premium']
                
                return {
                    'exp_values': np.exp(values / 100),
                    'log_values': np.log(values + 1),
                    'adjusted_prices': np.where(is_premium, prices * 1.2, prices)
                }
            
            numpy_complex_result, numpy_time = self.time_operation(
                "NumPy complex ops - NO SERIALIZATION (pure C)",
                numpy_complex
            )
            results['numpy'] = numpy_time
        
        # 4. Operations that DO cause serialization
        print(f"\n⚠️ OPERATIONS THAT CAUSE SERIALIZATION:")
        
        # Scalar extraction (serialization)
        if 'numpy' in conversions:
            def scalar_extraction():
                values = numpy_arrays['values']
                return {
                    'first_value': values[0],      # Serialization: C → Python
                    'max_value': np.max(values),   # No serialization: C aggregation
                    'value_at_1000': values[1000] if len(values) > 1000 else values[-1]  # Serialization
                }
            
            scalars, scalar_time = self.time_operation(
                "Scalar extraction - SERIALIZATION (C → Python)",
                scalar_extraction
            )
        
        # List conversion (mass serialization)
        if 'numpy' in conversions:
            def list_conversion():
                values = numpy_arrays['values']
                return values[:1000].tolist()  # Mass serialization: all elements
            
            lists, list_time = self.time_operation(
                "Array → List conversion - MASS SERIALIZATION",
                list_conversion
            )
        
        # String operations (full serialization)
        if 'pandas_arrow' in conversions:
            def string_operations():
                pdf = conversions['pandas_arrow'][0]
                return str(pdf.head())  # Full serialization for display
            
            strings, string_time = self.time_operation(
                "DataFrame → String - FULL SERIALIZATION",
                string_operations
            )
        
        print(f"\n📊 COMPLEX OPERATIONS PERFORMANCE:")
        if results:
            fastest_time = min(results.values())
            for framework, time_taken in results.items():
                speedup = time_taken / fastest_time
                print(f"   {framework:15}: {time_taken:.4f}s ({speedup:.1f}x)")
        
        return results

    def demo_arrow_benefits(self, spark_df):
        """Demonstrate where Arrow provides benefits vs overhead"""
        print("\n" + "="*60)
        print("🏹 ARROW BENEFITS VS OVERHEAD ANALYSIS")
        print("="*60)
        
        print("💡 ARROW ANALYSIS:")
        print("   - Arrow optimizes columnar data transfer")
        print("   - Benefits: Vectorized serialization, less memory copying")
        print("   - Overhead: Format conversion, not always zero-copy")
        
        # Test different data sizes to show Arrow's benefits
        sizes = [1000, 10000, 50000, 100000]
        arrow_benefits = {}
        
        for size in sizes:
            if size > self.rows:
                continue
                
            print(f"\n🔍 Testing with {size:,} rows:")
            
            # Create subset
            subset_df = spark_df.limit(size)
            
            # Without Arrow
            def without_arrow():
                no_arrow_df = self.spark_no_arrow.createDataFrame(subset_df.collect())
                return no_arrow_df.toPandas()
            
            _, no_arrow_time = self.time_operation(
                f"  No Arrow ({size:,} rows)",
                without_arrow
            )
            
            # With Arrow
            def with_arrow():
                return subset_df.toPandas()
            
            _, arrow_time = self.time_operation(
                f"  With Arrow ({size:,} rows)",
                with_arrow
            )
            
            speedup = no_arrow_time / arrow_time if arrow_time > 0 else 1
            print(f"    Arrow speedup (Spark → pandas): {speedup:.1f}x")

            # Compute benchmarks across frameworks on the same subset
            size_metrics = {
                'conversion': {
                    'no_arrow': no_arrow_time,
                    'arrow': arrow_time,
                },
                'compute': {},
                'total': {},
            }

            # Spark compute (no serialization)
            def spark_compute():
                df = subset_df.select(
                    (col("values") * col("prices")).alias("total_value"),
                    (col("revenue") * (1 + col("profit_margin") / 100)).alias("adjusted_revenue"),
                    F.sqrt(col("values")).alias("sqrt_values"),
                    (col("quantities") + col("values") * 2).alias("weighted_qty")
                )
                return df.count()

            _, spark_compute_time = self.time_operation(
                f"  Spark compute ({size:,} rows)",
                spark_compute
            )
            size_metrics['compute']['spark'] = spark_compute_time

            # Pandas compute (using Arrow-converted pandas)
            def pandas_convert_arrow():
                return subset_df.toPandas()

            pandas_df_arrow, _ = self.time_operation(
                f"  Convert (Arrow) pandas ready ({size:,} rows)",
                pandas_convert_arrow
            )

            def pandas_compute():
                pdf = pandas_df_arrow.copy()
                pdf['total_value'] = pdf['values'] * pdf['prices']
                pdf['adjusted_revenue'] = pdf['revenue'] * (1 + pdf['profit_margin'] / 100)
                pdf['sqrt_values'] = np.sqrt(pdf['values'])
                pdf['weighted_qty'] = pdf['quantities'] + pdf['values'] * 2
                return len(pdf)

            _, pandas_compute_time = self.time_operation(
                f"  Pandas compute ({size:,} rows)",
                pandas_compute
            )
            size_metrics['compute']['pandas'] = pandas_compute_time
            size_metrics['total']['pandas_arrow'] = arrow_time + pandas_compute_time

            # Pandas compute after no-Arrow path
            def pandas_convert_no_arrow():
                no_arrow_df = self.spark_no_arrow.createDataFrame(subset_df.collect())
                return no_arrow_df.toPandas()

            pandas_df_no_arrow, _ = self.time_operation(
                f"  Convert (No Arrow) pandas ready ({size:,} rows)",
                pandas_convert_no_arrow
            )

            def pandas_compute_no_arrow():
                pdf = pandas_df_no_arrow.copy()
                pdf['total_value'] = pdf['values'] * pdf['prices']
                pdf['adjusted_revenue'] = pdf['revenue'] * (1 + pdf['profit_margin'] / 100)
                pdf['sqrt_values'] = np.sqrt(pdf['values'])
                pdf['weighted_qty'] = pdf['quantities'] + pdf['values'] * 2
                return len(pdf)

            _, pandas_compute_time_no_arrow = self.time_operation(
                f"  Pandas compute (No Arrow path) ({size:,} rows)",
                pandas_compute_no_arrow
            )
            size_metrics['total']['pandas_no_arrow'] = no_arrow_time + pandas_compute_time_no_arrow

            # NumPy compute (from pandas via Arrow)
            def numpy_prepare():
                pdf = pandas_df_arrow
                return (
                    pdf['values'].values,
                    pdf['prices'].values,
                    pdf['revenue'].values,
                    pdf['profit_margin'].values,
                    pdf['quantities'].values,
                )

            numpy_inputs, _ = self.time_operation(
                f"  Prepare NumPy arrays ({size:,} rows)",
                numpy_prepare
            )

            def numpy_compute():
                values, prices, revenue, margin, quantities = numpy_inputs
                total_value = values * prices
                adjusted_revenue = revenue * (1 + margin / 100)
                sqrt_values = np.sqrt(values)
                weighted_qty = quantities + values * 2
                # Prevent lazy elimination by returning a small reduction
                return (
                    float(total_value.mean())
                    + float(adjusted_revenue.mean())
                    + float(sqrt_values.mean())
                    + float(weighted_qty.mean())
                )

            _, numpy_compute_time = self.time_operation(
                f"  NumPy compute ({size:,} rows)",
                numpy_compute
            )
            size_metrics['compute']['numpy'] = numpy_compute_time
            size_metrics['total']['numpy_arrow'] = arrow_time + numpy_compute_time
            size_metrics['total']['numpy_no_arrow'] = no_arrow_time + numpy_compute_time

            # Jitted NumPy compute (if available)
            if NUMBA_AVAILABLE:
                @njit
                def jitted(values, prices, revenue, margin, quantities):
                    n = len(values)
                    s = 0.0
                    for i in range(n):
                        tv = values[i] * prices[i]
                        ar = revenue[i] * (1 + margin[i] / 100)
                        sv = (values[i]) ** 0.5
                        wq = quantities[i] + values[i] * 2.0
                        s += tv + ar + sv + wq
                    return s / n

                # Warm-up
                vals_small = tuple(arr[:100] for arr in numpy_inputs)
                _ = jitted(*vals_small)

                def numba_compute():
                    return jitted(*numpy_inputs)

                _, numba_compute_time = self.time_operation(
                    f"  Jitted NumPy compute ({size:,} rows)",
                    numba_compute
                )
                size_metrics['compute']['numba'] = numba_compute_time
                size_metrics['total']['numba_arrow'] = arrow_time + numba_compute_time
                size_metrics['total']['numba_no_arrow'] = no_arrow_time + numba_compute_time

            # Pandas-on-Spark compute (if available)
            if self.pandas_on_spark_available:
                try:
                    import pyspark.pandas as ps

                    def ps_compute():
                        ps_df = ps.DataFrame(subset_df)
                        ps_df = ps_df.assign(
                            total_value=ps_df['values'] * ps_df['prices'],
                            adjusted_revenue=ps_df['revenue'] * (1 + ps_df['profit_margin'] / 100),
                            sqrt_values=ps_df['values'] ** 0.5,
                            weighted_qty=ps_df['quantities'] + ps_df['values'] * 2,
                        )
                        return ps_df.count()

                    _, ps_compute_time = self.time_operation(
                        f"  Pandas-on-Spark compute ({size:,} rows)",
                        ps_compute
                    )
                    size_metrics['compute']['pandas_on_spark'] = ps_compute_time
                except Exception as e:
                    print(f"    ⚠️ Pandas-on-Spark compute failed: {e}")

            arrow_benefits[size] = size_metrics
        
        print(f"\n📊 ARROW SCALING ANALYSIS:")
        for size, metrics in arrow_benefits.items():
            conv = metrics['conversion']
            comp = metrics['compute']
            total = metrics['total']
            arrow_speedup = conv['no_arrow'] / conv['arrow'] if conv['arrow'] > 0 else 1
            print(f"   {size:6,} rows:")
            print(f"      Spark→pandas Arrow speedup: {arrow_speedup:4.1f}x")
            if comp:
                # Show compute comparisons
                for k, v in comp.items():
                    print(f"      Compute {k:15}: {v:.4f}s")
            if total:
                # Show total times for popular paths
                if 'pandas_arrow' in total:
                    print(f"      Total pandas (Arrow): {total['pandas_arrow']:.4f}s")
                if 'pandas_no_arrow' in total:
                    print(f"      Total pandas (NoArrow): {total['pandas_no_arrow']:.4f}s")
                if 'numpy_arrow' in total:
                    print(f"      Total NumPy (Arrow):  {total['numpy_arrow']:.4f}s")
                if 'numpy_no_arrow' in total:
                    print(f"      Total NumPy (NoArrow):{total['numpy_no_arrow']:.4f}s")
                if 'numba_arrow' in total:
                    print(f"      Total Numba (Arrow):  {total['numba_arrow']:.4f}s")
                if 'numba_no_arrow' in total:
                    print(f"      Total Numba (NoArrow):{total['numba_no_arrow']:.4f}s")
        
        return arrow_benefits

    def run_comprehensive_comparison(self):
        """Run the complete framework comparison"""
        try:
            # Create initial data in Spark
            spark_df = self.create_initial_data()
            
            # Convert to all frameworks
            conversions = self.convert_to_frameworks(spark_df)
            
            # Compare arithmetic operations
            arithmetic_results = self.demo_arithmetic_operations(spark_df, conversions)
            
            # Compare aggregation operations
            aggregation_results = self.demo_aggregation_operations(spark_df, conversions)
            
            # Compare complex operations and serialization
            complex_results = self.demo_complex_operations(spark_df, conversions)
            
            # Analyze Arrow benefits
            arrow_results = self.demo_arrow_benefits(spark_df)
            
            # Final summary
            self.print_final_summary(arithmetic_results, aggregation_results, 
                                   complex_results, arrow_results, conversions)
            
        except Exception as e:
            print(f"❌ Error during comparison: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def print_final_summary(self, arithmetic_results, aggregation_results, 
                          complex_results, arrow_results, conversions):
        """Print comprehensive comparison summary"""
        print("\n" + "="*60)
        print("🏆 COMPREHENSIVE FRAMEWORK COMPARISON SUMMARY")
        print("="*60)
        
        print("\n🎯 KEY FINDINGS:")
        print("   • In Spark: prefer native Spark. If converting, use Arrow → pandas and keep vectorized.")
        print("   • NumPy/Numba: use only for narrow hotspots that pandas cannot express efficiently.")
        
        print("\n⚡ PERFORMANCE HIERARCHY (typical):")
        print("   1. Jitted NumPy (Numba)   - Fastest computation")
        print("   2. NumPy (vectorized)     - Fast C operations")
        print("   3. Pandas (vectorized)    - Optimized single-machine")
        print("   4. Spark (distributed)    - Scales to large data")
        print("   5. Pandas-on-Spark        - Convenient but overhead")
        
        print("\n🔄 SERIALIZATION COSTS:")
        if conversions:
            print("   Conversion times from Spark:")
            for name, (_, time_taken) in conversions.items():
                print(f"     {name:20}: {time_taken:.4f}s")
        
        print("\n🏹 ARROW BENEFITS:")
        if arrow_results:
            speedups = []
            for size, metrics in arrow_results.items():
                conv = metrics.get('conversion', {})
                no_arrow = conv.get('no_arrow')
                arrow = conv.get('arrow')
                if no_arrow is not None and arrow and arrow > 0:
                    speedups.append(no_arrow / arrow)
            if speedups:
                avg_speedup = float(np.mean(speedups))
                print(f"   Average Arrow speedup: {avg_speedup:.1f}x")
            else:
                print("   Average Arrow speedup: N/A")
            print("   • Most beneficial for: Large datasets, wide tables")
            print("   • Less beneficial for: Small datasets, simple operations")
        
        print("\n💡 DECISION FRAMEWORK:")
        print("\n✅ USE NUMPY WHEN:")
        print("   • Single-machine data fits in memory")
        print("   • Heavy mathematical computations")
        print("   • Maximum performance for numerical operations")
        print("   • Simple data structures (arrays)")
        
        print("\n✅ USE PANDAS WHEN:")
        print("   • Single-machine data with complex structure")
        print("   • Data manipulation and cleaning")
        print("   • Integration with existing pandas ecosystem")
        print("   • Time series and statistical analysis")
        
        print("\n✅ USE SPARK WHEN:")
        print("   • Data too large for single machine")
        print("   • Distributed computing required")
        print("   • Integration with big data ecosystem")
        print("   • Fault tolerance and scalability needed")
        
        print("\n✅ USE JITTED NUMPY (NUMBA) WHEN:")
        print("   • Custom algorithms not vectorizable")
        print("   • Complex loops and conditionals")
        print("   • Maximum performance for specialized operations")
        print("   • Can amortize JIT compilation cost")
        
        print("\n✅ USE ARROW WHEN:")
        print("   • Converting between Spark and pandas")
        print("   • Large datasets with columnar operations")
        print("   • Cross-language data exchange")
        print("   • Memory efficiency is critical")
        
        print("\n⚠️ SERIALIZATION HOTSPOTS TO AVOID:")
        print("   • Frequent scalar extraction from arrays")
        print("   • Unnecessary .tolist() conversions")
        print("   • Mixing frameworks in tight loops")
        print("   • String representations of large arrays")
        
        print("\n🎯 GOLDEN RULES:")
        print("   1. 'Right tool for the right job'")
        print("   2. 'Stay within one framework as long as possible'")
        print("   3. 'Measure before optimizing'")
        print("   4. 'Consider total cost: computation + conversion'")
        print("   5. 'Use Arrow for Spark ↔ pandas conversions'")

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark_no_arrow.stop()
        self.spark_with_arrow.stop()
        print("   ✅ Stopped Spark sessions")
        print("\n👋 Framework comparison completed!")


def main():
    """Main function to run the comprehensive framework comparison"""
    print("🚀 Starting Comprehensive Framework Comparison...")
    
    # Check system resources
    memory_gb = psutil.virtual_memory().total / (1024**3)
    print(f"💻 System: {memory_gb:.1f}GB RAM")
    
    # Check dependencies
    print(f"✅ NumPy: {np.__version__}")
    print(f"✅ Pandas: {pd.__version__}")
    if NUMBA_AVAILABLE:
        print(f"✅ Numba: {numba.__version__}")
    else:
        print("⚠️ Numba not available")
    
    # Adjust size based on available memory
    if memory_gb < 8:
        rows = 100_000
    elif memory_gb < 16:
        rows = 200_000
    else:
        rows = 300_000
    
    comparison = FrameworkComparison(rows=rows)
    comparison.run_comprehensive_comparison()


if __name__ == "__main__":
    import os as _os, sys as _sys
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/01_frameworks_conclusion.md",
            title="Frameworks: Conclusion first (Spark, pandas, NumPy, Numba)",
            main_callable=main,
        )
    else:
        main()

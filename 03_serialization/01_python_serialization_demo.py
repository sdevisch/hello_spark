#!/usr/bin/env python3
"""
Conclusion first: Use Arrow for Spark↔pandas; avoid Python UDFs
===============================================================

Conclusion: In a Spark context, when moving to pandas, enable Arrow. Avoid
Python UDFs; prefer native Spark functions. Use pandas/NumPy only after an
Arrow conversion when you need single-machine analysis.

Why: Arrow gives 2–10x faster transfers; native functions avoid JVM↔Python
serialization. Pandas/NumPy excel once data is local.

What: Minimal demonstrations of Arrow vs no-Arrow and UDF cost.

How: Create Spark DataFrames, compare conversions and compute routes.
"""

import time
import os
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyarrow as pa
import pyarrow.parquet as pq

class SerializationBenchmark:
    def __init__(self):
        """Initialize Spark sessions with and without Arrow"""
        print("🚀 PYTHON SERIALIZATION PERFORMANCE DEMO")
        print("=" * 60)
        
        # Spark session WITHOUT Arrow (traditional serialization)
        self.spark_no_arrow = SparkSession.builder \
            .appName("NoArrow-SerializationDemo") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .getOrCreate()
        
        self.spark_no_arrow.sparkContext.setLogLevel("WARN")
        
        # Spark session WITH Arrow (optimized serialization)
        self.spark_with_arrow = SparkSession.builder \
            .appName("WithArrow-SerializationDemo") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .config("spark.sql.execution.arrow.maxRecordsPerBatch", "10000") \
            .getOrCreate()
        
        self.spark_with_arrow.sparkContext.setLogLevel("WARN")
        
        print(f"🌐 Spark UI (No Arrow): http://localhost:4040")
        print(f"🌐 Spark UI (With Arrow): http://localhost:4041") 
        print("=" * 60)

    def time_operation(self, operation_name, func, *args, **kwargs):
        """Time an operation and return results with timing"""
        print(f"⏱️  {operation_name}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ✅ Completed in {duration:.3f}s")
        return result, duration

    def demo_1_basic_pandas_creation(self):
        """Demonstrate basic pandas DataFrame creation performance"""
        print("\n" + "="*60)
        print("📊 DEMO 1: BASIC PANDAS DATAFRAME CREATION")
        print("="*60)
        
        # Test different data sizes
        sizes = [10_000, 100_000, 1_000_000]
        
        for size in sizes:
            print(f"\n📈 Testing with {size:,} rows:")
            
            # Method 1: Using Python lists (slow)
            def create_with_lists():
                data = {
                    'id': list(range(size)),
                    'value': [np.random.random() for _ in range(size)],
                    'category': ['A' if i % 2 == 0 else 'B' for i in range(size)]
                }
                return pd.DataFrame(data)
            
            # Method 2: Using NumPy arrays (fast)
            def create_with_numpy():
                data = {
                    'id': np.arange(size),
                    'value': np.random.random(size),
                    'category': np.where(np.arange(size) % 2 == 0, 'A', 'B')
                }
                return pd.DataFrame(data)
            
            _, list_time = self.time_operation(
                "🐌 SLOW - Python lists", create_with_lists
            )
            
            _, numpy_time = self.time_operation(
                "🚀 FAST - NumPy arrays", create_with_numpy
            )
            
            speedup = list_time / numpy_time
            print(f"   📈 Speedup: {speedup:.1f}x faster with NumPy")

    def demo_2_spark_to_pandas_conversion(self):
        """Demonstrate Spark to pandas conversion with and without Arrow"""
        print("\n" + "="*60)
        print("🔄 DEMO 2: SPARK TO PANDAS CONVERSION")
        print("="*60)
        
        # Create test data sizes
        sizes = [50_000, 200_000, 500_000]
        
        for size in sizes:
            print(f"\n📊 Testing with {size:,} rows:")
            
            # Create Spark DataFrame with mixed data types
            spark_df_no_arrow = self.spark_no_arrow.range(size).select(
                col("id"),
                (rand() * 100).alias("float_col"),
                (rand() * 1000).cast("int").alias("int_col"),
                when(rand() > 0.5, "Category_A").otherwise("Category_B").alias("string_col"),
                (rand() > 0.7).alias("bool_col")
            )
            
            spark_df_with_arrow = self.spark_with_arrow.range(size).select(
                col("id"),
                (rand() * 100).alias("float_col"),
                (rand() * 1000).cast("int").alias("int_col"),
                when(rand() > 0.5, "Category_A").otherwise("Category_B").alias("string_col"),
                (rand() > 0.7).alias("bool_col")
            )
            
            # Test conversion WITHOUT Arrow
            _, no_arrow_time = self.time_operation(
                "🐌 SLOW - Without Arrow serialization",
                lambda: spark_df_no_arrow.toPandas()
            )
            
            # Test conversion WITH Arrow
            _, arrow_time = self.time_operation(
                "🚀 FAST - With Arrow serialization",
                lambda: spark_df_with_arrow.toPandas()
            )
            
            speedup = no_arrow_time / arrow_time
            print(f"   📈 Speedup: {speedup:.1f}x faster with Arrow")
            
            # Memory usage comparison
            print(f"   💾 Arrow reduces serialization overhead significantly!")

    def demo_3_udf_serialization_overhead(self):
        """Demonstrate UDF serialization overhead"""
        print("\n" + "="*60)
        print("🐍 DEMO 3: UDF SERIALIZATION OVERHEAD")
        print("="*60)
        
        size = 300_000
        print(f"📊 Testing with {size:,} rows:")
        
        # Create test data
        df_no_arrow = self.spark_no_arrow.range(size).select(
            col("id"),
            (rand() * 100).alias("value")
        )
        
        df_with_arrow = self.spark_with_arrow.range(size).select(
            col("id"),
            (rand() * 100).alias("value")
        )
        
        # Define Python UDF (requires serialization)
        def complex_python_function(value):
            """Complex Python function that requires serialization"""
            import math
            return math.sqrt(value) * 2 + math.sin(value)
        
        python_udf = udf(complex_python_function, DoubleType())
        
        print("\n🐌 SLOW - Python UDF (requires serialization):")
        
        # Without Arrow
        _, udf_no_arrow_time = self.time_operation(
            "   Without Arrow",
            lambda: df_no_arrow.select("id", python_udf("value").alias("result")).count()
        )
        
        # With Arrow
        _, udf_arrow_time = self.time_operation(
            "   With Arrow",
            lambda: df_with_arrow.select("id", python_udf("value").alias("result")).count()
        )
        
        print("\n🚀 FAST - Native Spark functions (no serialization):")
        
        # Native Spark equivalent (no serialization needed)
        _, native_time = self.time_operation(
            "   Native Spark functions",
            lambda: df_with_arrow.select(
                "id", 
                (sqrt("value") * 2 + sin("value")).alias("result")
            ).count()
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   Python UDF (No Arrow):  {udf_no_arrow_time:.3f}s")
        print(f"   Python UDF (With Arrow): {udf_arrow_time:.3f}s")
        print(f"   Native Spark:           {native_time:.3f}s")
        
        udf_speedup = udf_no_arrow_time / udf_arrow_time
        native_speedup = udf_no_arrow_time / native_time
        
        print(f"   Arrow UDF Speedup:      {udf_speedup:.1f}x")
        print(f"   Native vs UDF Speedup:  {native_speedup:.1f}x")

    def demo_4_memory_efficient_operations(self):
        """Demonstrate memory-efficient operations"""
        print("\n" + "="*60)
        print("💾 DEMO 4: MEMORY-EFFICIENT OPERATIONS")
        print("="*60)
        
        size = 400_000
        print(f"📊 Testing with {size:,} rows:")
        
        # Create large dataset
        df = self.spark_with_arrow.range(size).select(
            col("id"),
            (rand() * 1000).alias("value1"),
            (rand() * 1000).alias("value2"),
            (rand() * 1000).alias("value3"),
            when(rand() > 0.5, "A").otherwise("B").alias("category")
        )
        
        print("\n🐌 SLOW - Convert entire DataFrame to pandas:")
        
        # Method 1: Convert entire DataFrame (memory intensive)
        _, full_conversion_time = self.time_operation(
            "   Full DataFrame conversion",
            lambda: df.toPandas()
        )
        
        print("\n🚀 FAST - Use Spark operations then convert result:")
        
        # Method 2: Use Spark for heavy lifting, then convert small result
        _, optimized_time = self.time_operation(
            "   Spark aggregation + small conversion",
            lambda: df.groupBy("category") \
                     .agg(avg("value1").alias("avg_val1"),
                          avg("value2").alias("avg_val2"),
                          count("*").alias("count")) \
                     .toPandas()
        )
        
        speedup = full_conversion_time / optimized_time
        print(f"\n📈 RESULTS:")
        print(f"   Full conversion:     {full_conversion_time:.3f}s")
        print(f"   Optimized approach:  {optimized_time:.3f}s")
        print(f"   Speedup:            {speedup:.1f}x faster")
        print(f"   💡 Tip: Do heavy work in Spark, convert only final results!")

    def demo_5_arrow_specific_benefits(self):
        """Demonstrate Arrow-specific benefits"""
        print("\n" + "="*60)
        print("🏹 DEMO 5: ARROW-SPECIFIC BENEFITS")
        print("="*60)
        
        size = 200_000
        
        # Create DataFrame with complex data types
        df = self.spark_with_arrow.range(size).select(
            col("id"),
            array(lit(1), lit(2), lit(3)).alias("array_col"),
            create_map(lit("key1"), rand(), lit("key2"), rand()).alias("map_col"),
            struct(
                (rand() * 100).alias("x"),
                (rand() * 100).alias("y")
            ).alias("struct_col")
        )
        
        print(f"📊 Testing complex data types with {size:,} rows:")
        
        # Test with Arrow disabled
        df_no_arrow = self.spark_no_arrow.range(size).select(
            col("id"),
            array(lit(1), lit(2), lit(3)).alias("array_col"),
            create_map(lit("key1"), rand(), lit("key2"), rand()).alias("map_col"),
            struct(
                (rand() * 100).alias("x"),
                (rand() * 100).alias("y")
            ).alias("struct_col")
        )
        
        _, no_arrow_complex_time = self.time_operation(
            "🐌 SLOW - Complex types without Arrow",
            lambda: df_no_arrow.toPandas()
        )
        
        _, arrow_complex_time = self.time_operation(
            "🚀 FAST - Complex types with Arrow",
            lambda: df.toPandas()
        )
        
        speedup = no_arrow_complex_time / arrow_complex_time
        print(f"\n📈 RESULTS:")
        print(f"   Without Arrow: {no_arrow_complex_time:.3f}s")
        print(f"   With Arrow:    {arrow_complex_time:.3f}s")
        print(f"   Speedup:       {speedup:.1f}x faster")
        print(f"   💡 Arrow excels with complex nested data types!")

    def run_all_demos(self):
        """Run all serialization demonstrations"""
        try:
            self.demo_1_basic_pandas_creation()
            self.demo_2_spark_to_pandas_conversion()
            self.demo_3_udf_serialization_overhead()
            self.demo_4_memory_efficient_operations()
            self.demo_5_arrow_specific_benefits()
            
            print("\n" + "="*60)
            print("🎉 ALL SERIALIZATION DEMOS COMPLETED!")
            print("="*60)
            
            print("\n🎯 KEY TAKEAWAYS:")
            print("1. 📊 Use NumPy arrays instead of Python lists for pandas")
            print("2. 🏹 Enable Arrow for 2-10x faster Spark-pandas conversions")
            print("3. 🐍 Avoid Python UDFs - use native Spark functions when possible")
            print("4. 💾 Do heavy computation in Spark, convert only final results")
            print("5. 🔧 Arrow provides biggest benefits with complex data types")
            print("6. ⚡ Arrow reduces serialization overhead between JVM and Python")
            
            print(f"\n🌐 Explore Spark UIs:")
            print(f"   No Arrow:  http://localhost:4040")
            print(f"   With Arrow: http://localhost:4041")
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark_no_arrow.stop()
        self.spark_with_arrow.stop()
        print("   ✅ Stopped all Spark sessions")
        print("\n👋 Serialization demo completed!")


def main():
    """Main function to run the serialization demonstration"""
    # Check if required packages are available
    try:
        import pyarrow
        print(f"✅ PyArrow version: {pyarrow.__version__}")
    except ImportError:
        print("❌ PyArrow not found. Install with: pip install pyarrow")
        return
    
    try:
        import pandas
        print(f"✅ Pandas version: {pandas.__version__}")
    except ImportError:
        print("❌ Pandas not found. Install with: pip install pandas")
        return
    
    print(f"✅ NumPy version: {np.__version__}")
    
    benchmark = SerializationBenchmark()
    benchmark.run_all_demos()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/ser_01_python_serialization_demo.md",
            title="Serialization 01: Arrow vs traditional and UDF overhead",
            main_callable=main,
        )
    else:
        main()

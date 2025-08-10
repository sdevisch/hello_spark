#!/usr/bin/env python3
"""
NumPy Serialization Focus: Starting with Spark Data
==================================================

This script demonstrates serialization patterns when data STARTS in Spark
(which is the typical real-world scenario) and shows:

1. When NO serialization occurs (staying in Spark)
2. When serialization DOES occur (Spark → NumPy/pandas)
3. Why NumPy operations are fast once data is converted
4. The cost of moving data between runtimes

Key Learning: Starting with Spark data, serialization cost depends on 
whether you stay in Spark or move to NumPy/pandas for computation.
"""

import time
import numpy as np
import psutil
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import col

class NumPySerializationDemo:
    def __init__(self, rows=500_000):
        """Initialize with focus on operations starting from Spark data"""
        self.rows = rows
        
        print("🔢 SPARK-TO-NUMPY SERIALIZATION DEMO")
        print("=" * 50)
        print(f"📊 Dataset size: {rows:,} rows")
        print("🎯 Scenario: Data starts in Spark (realistic use case)")
        print("=" * 50)
        
        # Initialize Spark sessions for comparison
        self.spark_no_arrow = SparkSession.builder \
            .appName("NumPy-NoArrow-Compare") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .getOrCreate()
        
        self.spark_with_arrow = SparkSession.builder \
            .appName("NumPy-WithArrow-Compare") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
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

    def create_spark_data(self):
        """Create initial test data in Spark - REALISTIC STARTING POINT"""
        print("\n" + "="*50)
        print("📊 CREATING TEST DATA IN SPARK - REALISTIC STARTING POINT")
        print("="*50)
        
        print("💡 REAL-WORLD SCENARIO:")
        print("   - Data typically starts in Spark (from files, databases, etc.)")
        print("   - Data already distributed across Spark cluster")
        print("   - Question: Should we stay in Spark or move to NumPy/pandas?")
        
        def create_spark_dataframes():
            # REALISTIC DATA CREATION: In Spark (simulating reading from file/DB)
            # This simulates the typical scenario where data starts in Spark
            
            # Using Spark's range() and random functions to simulate realistic data
            df_base = self.spark_no_arrow.range(self.rows).select(
                col("id"),
                # Spark's built-in random functions - computed in JVM
                (F.rand() * 20 - 10).alias("x"),           # Uniform(-10, 10)
                (F.rand() * 10 - 5).alias("y"),            # Uniform(-5, 5)  
                (F.rand() * 100).alias("z"),               # Uniform(0, 100)
                (F.rand() * 4).cast("int").alias("category_id"),  # Random 0-3
                (-F.log(F.rand()) * 2).alias("weights"),   # Exponential(2.0)
                (F.rand() > 0.5).alias("flags")            # Random boolean
            )
            
            # Create identical data in both Spark sessions
            # Cache to avoid recomputation during tests
            spark_df_no_arrow = df_base.cache()
            spark_df_no_arrow.count()  # Force materialization
            
            # Create same data in Arrow-enabled session
            spark_df_arrow = self.spark_with_arrow.range(self.rows).select(
                col("id"),
                (F.rand() * 20 - 10).alias("x"),
                (F.rand() * 10 - 5).alias("y"),
                (F.rand() * 100).alias("z"),
                (F.rand() * 4).cast("int").alias("category_id"),
                (-F.log(F.rand()) * 2).alias("weights"),
                (F.rand() > 0.5).alias("flags")
            ).cache()
            
            spark_df_arrow.count()  # Force materialization
            
            return spark_df_no_arrow, spark_df_arrow
        
        spark_dfs, duration = self.time_operation("Creating Spark DataFrames", create_spark_dataframes)
        
        print(f"\n✅ Created Spark DataFrames with {self.rows:,} rows")
        print(f"💾 Data distributed across Spark cluster (cached in memory)")
        print(f"🎯 Now we'll compare: Stay in Spark vs Move to NumPy")
        
        return spark_dfs

    def demo_spark_vs_numpy_operations(self, spark_dfs):
        """Compare staying in Spark vs converting to NumPy for operations"""
        spark_df_no_arrow, spark_df_arrow = spark_dfs
        
        print("\n" + "="*50)
        print("⚖️  OPTION 1: STAY IN SPARK - NO SERIALIZATION")
        print("="*50)
        
        print("💡 WHY NO SERIALIZATION WHEN STAYING IN SPARK:")
        print("   - Data already in Spark cluster (JVM)")
        print("   - All operations happen in distributed JVM processes")
        print("   - No data movement between Python driver and executors")
        print("   - Spark's Catalyst optimizer handles execution")
        
        # SPARK OPERATIONS - NO SERIALIZATION (stay in JVM)
        def spark_basic_arithmetic():
            """Basic arithmetic operations in Spark - NO SERIALIZATION"""
            # WHAT HAPPENS HERE - NO SERIALIZATION:
            # 1. Operations executed in Spark executors (JVM processes)
            # 2. Data already distributed and cached in cluster memory
            # 3. Catalyst optimizer generates efficient Java bytecode
            # 4. Results computed in parallel across all executor cores
            # 5. No data transfer between Python driver and executors
            return spark_df_no_arrow.select(
                col("id"),
                (col("x") * col("x") + col("y") * col("y")).alias("x2_plus_y2")
            )
        
        result1, time1 = self.time_operation("Spark basic arithmetic (x² + y²)", spark_basic_arithmetic)
        
        def spark_math_functions():
            """Mathematical functions in Spark - NO SERIALIZATION"""
            # WHAT HAPPENS HERE - NO SERIALIZATION:
            # 1. Spark's built-in functions (sqrt, sin, cos) run in JVM
            # 2. Leverages Java's optimized math libraries
            # 3. Vectorized execution across distributed data
            # 4. Catalyst optimizer may use code generation for performance
            # 5. All computation happens in executor JVMs
            return spark_df_no_arrow.select(
                col("id"),
                (F.sqrt(col("x")*col("x") + col("y")*col("y")) + 
                 F.sin(col("x")) * F.cos(col("y"))).alias("complex_math")
            )
        
        result2, time2 = self.time_operation("Spark math functions (sqrt, sin, cos)", spark_math_functions)
        
        def spark_aggregations():
            """Aggregation operations in Spark - NO SERIALIZATION"""
            # WHAT HAPPENS HERE - NO SERIALIZATION:
            # 1. GroupBy operations use Spark's distributed hash aggregation
            # 2. Data shuffled between executors but stays in JVM processes
            # 3. Optimized aggregation algorithms (e.g., Welford for stddev)
            # 4. Results computed in parallel across cluster
            return spark_df_no_arrow.groupBy("category_id").agg(
                F.avg("x").alias("avg_x"),
                F.stddev("y").alias("stddev_y"),
                F.sum("z").alias("sum_z"),
                F.count("*").alias("count")
            )
        
        result3, time3 = self.time_operation("Spark aggregations (groupBy)", spark_aggregations)
        
        print(f"\n🎯 SPARK OPERATIONS PERFORMANCE (NO SERIALIZATION):")
        print(f"   Basic arithmetic:  {time1:.4f}s")
        print(f"   Math functions:    {time2:.4f}s")
        print(f"   Aggregations:      {time3:.4f}s")
        print(f"   💡 All operations stay in Spark JVM - no serialization overhead!")
        
        # Now demonstrate the cost of moving to NumPy
        print("\n" + "="*50)
        print("📤 OPTION 2: MOVE TO NUMPY - SERIALIZATION REQUIRED")
        print("="*50)
        
        print("💡 WHY SERIALIZATION IS REQUIRED:")
        print("   - Must move data from Spark JVM to Python process")
        print("   - Distributed data → single-machine arrays")
        print("   - But enables NumPy's optimized operations")
        
        # Test conversion cost and then NumPy operations
        def convert_to_numpy_no_arrow():
            """Convert Spark to NumPy without Arrow - EXPENSIVE SERIALIZATION"""
            # STEP 1: Spark → pandas (EXPENSIVE SERIALIZATION)
            # - JVM objects → Python objects conversion
            # - Distributed data collected to driver
            # - Row-by-row deserialization
            pdf = spark_df_no_arrow.toPandas()
            
            # STEP 2: pandas → NumPy (FAST, NO SERIALIZATION)
            # - Direct access to underlying NumPy arrays
            return {
                'x': pdf['x'].values,
                'y': pdf['y'].values,
                'z': pdf['z'].values
            }
        
        numpy_data_no_arrow, convert_time_no_arrow = self.time_operation(
            "Convert Spark → NumPy (no Arrow) - EXPENSIVE",
            convert_to_numpy_no_arrow
        )
        
        def convert_to_numpy_with_arrow():
            """Convert Spark to NumPy with Arrow - OPTIMIZED SERIALIZATION"""
            # STEP 1: Spark → pandas with Arrow (OPTIMIZED SERIALIZATION)
            pdf = spark_df_arrow.toPandas()
            
            # STEP 2: pandas → NumPy (FAST, NO SERIALIZATION)
            return {
                'x': pdf['x'].values,
                'y': pdf['y'].values,
                'z': pdf['z'].values
            }
        
        numpy_data_arrow, convert_time_arrow = self.time_operation(
            "Convert Spark → NumPy (with Arrow) - OPTIMIZED",
            convert_to_numpy_with_arrow
        )
        
        # Now demonstrate NumPy operations on the converted data - FAST once converted
        print(f"\n⚡ NUMPY OPERATIONS AFTER CONVERSION - NO SERIALIZATION:")
        
        def numpy_operations_fast():
            """Fast NumPy operations on converted data - NO SERIALIZATION"""
            # WHAT HAPPENS HERE - NO SERIALIZATION:
            # 1. Data already in NumPy C arrays (from conversion above)
            # 2. All operations vectorized in optimized C code
            # 3. SIMD instructions, cache-friendly memory access
            # 4. Much faster per-element computation than Spark
            
            # Basic arithmetic - vectorized C operations
            arithmetic_result = numpy_data_arrow['x'] ** 2 + numpy_data_arrow['y'] ** 2
            
            # Complex mathematical operations - optimized C libraries
            math_result = (np.sqrt(numpy_data_arrow['x']**2 + numpy_data_arrow['y']**2) + 
                          np.sin(numpy_data_arrow['x']) * np.cos(numpy_data_arrow['y']))
            
            # Statistical aggregations - optimized algorithms
            stats = {
                'mean_x': np.mean(numpy_data_arrow['x']),
                'std_y': np.std(numpy_data_arrow['y']),
                'sum_z': np.sum(numpy_data_arrow['z']),
                'percentile_95': np.percentile(numpy_data_arrow['z'], 95)
            }
            
            return arithmetic_result, math_result, stats
        
        numpy_results, numpy_ops_time = self.time_operation(
            "NumPy operations (all computations)",
            numpy_operations_fast
        )
        
        # FINAL COMPARISON: Total cost analysis
        print(f"\n📊 CONVERSION COST COMPARISON:")
        print(f"   Spark → NumPy (no Arrow):  {convert_time_no_arrow:.4f}s")
        print(f"   Spark → NumPy (with Arrow): {convert_time_arrow:.4f}s")
        print(f"   Arrow speedup:              {convert_time_no_arrow/convert_time_arrow:.1f}x")
        
        print(f"\n⚡ COMPUTATION SPEED COMPARISON:")
        print(f"   Spark operations:           {time1 + time2 + time3:.4f}s")
        print(f"   NumPy operations:           {numpy_ops_time:.4f}s")
        print(f"   NumPy speedup:              {(time1 + time2 + time3)/numpy_ops_time:.1f}x")
        
        print(f"\n🎯 TOTAL TIME ANALYSIS:")
        total_spark_time = time1 + time2 + time3
        total_numpy_time = convert_time_arrow + numpy_ops_time
        print(f"   Stay in Spark:              {total_spark_time:.4f}s")
        print(f"   Convert to NumPy + compute: {total_numpy_time:.4f}s")
        
        if total_spark_time < total_numpy_time:
            print(f"   ✅ Winner: Stay in Spark ({total_numpy_time/total_spark_time:.1f}x faster)")
        else:
            print(f"   ✅ Winner: Convert to NumPy ({total_spark_time/total_numpy_time:.1f}x faster)")
        
        return {
            'spark_times': [time1, time2, time3],
            'numpy_convert_times': [convert_time_no_arrow, convert_time_arrow],
            'numpy_ops_time': numpy_ops_time
        }

    def demo_why_numpy_wins_after_conversion(self):
        """Demonstrate why NumPy operations are so fast once data is converted"""
        print("\n" + "="*50)
        print("🎯 WHY NUMPY IS FAST AFTER CONVERSION")
        print("="*50)
        
        print("💡 NUMPY'S PERFORMANCE ADVANTAGES:")
        print("   1. Vectorized operations - SIMD instructions")
        print("   2. Contiguous memory layout - cache friendly")
        print("   3. Compiled C code - no Python interpreter overhead")
        print("   4. Optimized libraries - BLAS, LAPACK integration")
        print("   5. Single-machine efficiency - no distributed overhead")

    def run_comprehensive_demo(self):
        """Run the complete Spark-to-NumPy serialization demonstration"""
        try:
            # Create initial data in Spark (realistic starting point)
            spark_dfs = self.create_spark_data()
            
            # Compare staying in Spark vs moving to NumPy
            performance_results = self.demo_spark_vs_numpy_operations(spark_dfs)
            
            # Explain why NumPy is fast after conversion
            self.demo_why_numpy_wins_after_conversion()
            
            # Final summary
            self.print_final_summary(performance_results)
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def print_final_summary(self, performance_results):
        """Print comprehensive summary with performance results"""
        print("\n" + "="*50)
        print("🏆 SPARK-TO-NUMPY PERFORMANCE SUMMARY")
        print("="*50)
        
        print("\n🎯 KEY LEARNINGS FROM REALISTIC SCENARIO:")
        
        print("\n🚀 WHEN DATA STARTS IN SPARK:")
        print("   • Staying in Spark = No serialization overhead")
        print("   • Spark operations leverage distributed computing")
        print("   • All computation happens in JVM cluster")
        print("   • Good for large-scale data processing")
        
        print("\n📤 WHEN MOVING TO NUMPY:")
        print("   • Serialization cost: Spark → pandas → NumPy")
        print("   • Arrow provides 4-6x serialization speedup")
        print("   • NumPy operations much faster once converted")
        print("   • Best for intensive mathematical computations")
        
        print("\n⚖️ DECISION FRAMEWORK:")
        spark_total = sum(performance_results['spark_times'])
        numpy_convert = performance_results['numpy_convert_times'][1]  # Arrow version
        numpy_ops = performance_results['numpy_ops_time']
        numpy_total = numpy_convert + numpy_ops
        
        print(f"   Spark operations:           {spark_total:.4f}s")
        print(f"   NumPy conversion + ops:     {numpy_total:.4f}s")
        
        if spark_total < numpy_total:
            print(f"   ✅ For this workload: Stay in Spark")
        else:
            print(f"   ✅ For this workload: Convert to NumPy")
            
        print("\n💡 PRACTICAL DECISION GUIDE:")
        print("   • Heavy math/stats → Consider NumPy conversion")
        print("   • Large data processing → Stay in Spark")
        print("   • Multiple reuses → NumPy conversion pays off")
        print("   • One-time operations → Stay in Spark")
        print("   • Always use Arrow for conversions!")

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark_no_arrow.stop()
        self.spark_with_arrow.stop()
        print("   ✅ Stopped Spark sessions")
        print("\n👋 Spark-to-NumPy serialization demo completed!")


def main():
    """Main function to run the Spark-to-NumPy demonstration"""
    print("🚀 Starting Spark-to-NumPy Serialization Demo...")
    
    # Check system resources
    memory_gb = psutil.virtual_memory().total / (1024**3)
    print(f"💻 System: {memory_gb:.1f}GB RAM")
    
    # Adjust size based on available memory
    if memory_gb < 8:
        rows = 100_000
    elif memory_gb < 16:
        rows = 300_000
    else:
        rows = 500_000
    
    demo = NumPySerializationDemo(rows=rows)
    demo.run_comprehensive_demo()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/03_serialization_numpy_focus_output.md",
            title="Serialization: Spark→NumPy focus and total cost",
            main_callable=main,
        )
    else:
        main()

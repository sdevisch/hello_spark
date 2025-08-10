#!/usr/bin/env python3
"""
Spark Data Types Performance Comparison
=======================================

This script demonstrates the performance and memory differences between:
1. Reading everything as strings vs. correct data types
2. Using 64-bit data types vs. right-sized data types
3. Impact on Spark operations, memory usage, and processing speed

Key comparisons:
- String parsing vs native type operations
- Memory overhead of oversized data types
- Performance impact on aggregations, joins, and transformations
"""

import time
import numpy as np
import pandas as pd
import psutil
import os
from decimal import Decimal
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, avg, sum, count, max as spark_max
import matplotlib.pyplot as plt
import seaborn as sns
import os as _os

class SparkDataTypesDemo:
    def __init__(self, rows=500_000):  # Reduced for more stable measurements
        """Initialize Spark Data Types Performance Demo"""
        self.rows = rows
        self.results = {}
        
        print("🔢 SPARK DATA TYPES PERFORMANCE DEMO")
        print("=" * 50)
        print(f"📊 Dataset size: {rows:,} rows")
        print("🎯 Focus: Data type impact on performance & memory")
        print("=" * 50)
        
        # Initialize Spark session
        self.spark = SparkSession.builder \
            .appName("DataTypesPerformanceDemo") \
            .master("local[*]") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
        # Memory tracking setup
        self.process = psutil.Process(os.getpid())
        
        # Get Spark context for memory tracking
        self.sc = self.spark.sparkContext
        
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        import gc
        gc.collect()  # Force garbage collection for more accurate measurement
        
        # Get both process memory and Spark memory info
        process_memory = self.process.memory_info().rss / 1024 / 1024
        
        # Try to get Spark storage memory info
        try:
            status = self.sc.statusTracker()
            executor_infos = status.getExecutorInfos()
            spark_memory = sum(info.memoryUsed for info in executor_infos) / 1024 / 1024
            return {'process': process_memory, 'spark': spark_memory}
        except:
            return {'process': process_memory, 'spark': 0}
    
    def get_memory_difference(self, mem_before, mem_after):
        """Calculate memory difference focusing on Spark memory"""
        if isinstance(mem_before, dict) and isinstance(mem_after, dict):
            return mem_after['spark'] - mem_before['spark']
        else:
            return mem_after - mem_before
    
    def estimate_dataframe_size_mb(self, df):
        """Estimate DataFrame size in MB using schema and row count"""
        try:
            # Get schema information
            schema = df.schema
            row_count = df.count()
            
            # Estimate bytes per row based on data types
            bytes_per_row = 0
            for field in schema.fields:
                if field.dataType.typeName() == 'string':
                    bytes_per_row += 20  # Average string size estimate
                elif field.dataType.typeName() == 'long':
                    bytes_per_row += 8
                elif field.dataType.typeName() == 'double':
                    bytes_per_row += 8
                elif field.dataType.typeName() == 'integer':
                    bytes_per_row += 4
                elif field.dataType.typeName() == 'float':
                    bytes_per_row += 4
                elif field.dataType.typeName() == 'byte':
                    bytes_per_row += 1
                elif field.dataType.typeName() == 'boolean':
                    bytes_per_row += 1
                elif field.dataType.typeName() == 'timestamp':
                    bytes_per_row += 8
                else:
                    bytes_per_row += 8  # Default estimate
            
            total_bytes = bytes_per_row * row_count
            return total_bytes / (1024 * 1024)  # Convert to MB
        except:
            return 0
    
    def create_sample_data(self):
        """Create sample data for testing different scenarios"""
        print("📋 Creating sample datasets...")
        
        # Generate realistic data
        np.random.seed(42)
        
        data = {
            'id': range(1, self.rows + 1),
            'category_id': np.random.randint(1, 100, self.rows),  # Small int
            'price': np.random.uniform(1.0, 1000.0, self.rows),  # Float
            'quantity': np.random.randint(1, 50, self.rows),  # Small int
            'timestamp': pd.date_range('2023-01-01', periods=self.rows, freq='1s'),
            'status': np.random.choice(['active', 'inactive', 'pending'], self.rows),
            'score': np.random.uniform(0.0, 100.0, self.rows),  # Float
            'region_code': np.random.randint(1, 10, self.rows),  # Very small int
            'is_premium': np.random.choice([True, False], self.rows)
        }
        
        # Convert to pandas DataFrame first for easier manipulation
        df_pandas = pd.DataFrame(data)
        
        return df_pandas
    
    def scenario_1_strings_vs_correct_types(self):
        """Compare reading everything as strings vs correct data types"""
        print("\n🔸 SCENARIO 1: Strings vs Correct Data Types")
        print("-" * 40)
        
        df_pandas = self.create_sample_data()
        
        # Scenario 1A: Everything as strings (worst case)
        print("Testing: Everything as STRING types...")
        string_schema = StructType([
            StructField("id", StringType(), True),
            StructField("category_id", StringType(), True),
            StructField("price", StringType(), True),
            StructField("quantity", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("status", StringType(), True),
            StructField("score", StringType(), True),
            StructField("region_code", StringType(), True),
            StructField("is_premium", StringType(), True)
        ])
        
        # Convert all to strings
        df_strings = df_pandas.copy()
        for column_name in df_strings.columns:
            df_strings[column_name] = df_strings[column_name].astype(str)
        
        # Clear any existing cache
        self.spark.catalog.clearCache()
        
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        df_spark_strings = self.spark.createDataFrame(df_strings, schema=string_schema)
        df_spark_strings.cache()
        count_strings = df_spark_strings.count()  # Force materialization
        
        load_time_strings = time.time() - start_time
        # Wait a moment for memory to stabilize
        time.sleep(0.5)
        mem_after_strings = self.get_memory_usage()
        
        # Test operations with string data (requires casting)
        start_time = time.time()
        result_strings = df_spark_strings.select(
            avg(col("price").cast("double")).alias("avg_price"),
            sum(col("quantity").cast("int")).alias("total_quantity"),
            count(col("id")).alias("record_count")
        ).collect()
        operation_time_strings = time.time() - start_time
        
        # Scenario 1B: Correct data types
        print("Testing: CORRECT data types...")
        correct_schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("category_id", IntegerType(), True),
            StructField("price", DoubleType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("status", StringType(), True),
            StructField("score", DoubleType(), True),
            StructField("region_code", IntegerType(), True),
            StructField("is_premium", BooleanType(), True)
        ])
        
        # Clean up previous dataframe and clear cache
        df_spark_strings.unpersist()
        self.spark.catalog.clearCache()
        
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        df_spark_correct = self.spark.createDataFrame(df_pandas, schema=correct_schema)
        df_spark_correct.cache()
        count_correct = df_spark_correct.count()  # Force materialization
        
        load_time_correct = time.time() - start_time
        # Wait a moment for memory to stabilize
        time.sleep(0.5)
        mem_after_correct = self.get_memory_usage()
        
        # Test operations with correct types (no casting needed)
        start_time = time.time()
        result_correct = df_spark_correct.select(
            avg("price").alias("avg_price"),
            sum("quantity").alias("total_quantity"),
            count("id").alias("record_count")
        ).collect()
        operation_time_correct = time.time() - start_time
        
        # Estimate DataFrame sizes for memory comparison
        strings_size = self.estimate_dataframe_size_mb(df_spark_strings)
        correct_size = self.estimate_dataframe_size_mb(df_spark_correct)
        
        # Store results
        self.results['scenario_1'] = {
            'strings': {
                'load_time': load_time_strings,
                'operation_time': operation_time_strings,
                'memory_usage': strings_size,
                'total_time': load_time_strings + operation_time_strings
            },
            'correct_types': {
                'load_time': load_time_correct,
                'operation_time': operation_time_correct,
                'memory_usage': correct_size,
                'total_time': load_time_correct + operation_time_correct
            }
        }
        
        # Print results
        print(f"🔴 Strings approach:")
        print(f"   Load time: {load_time_strings:.3f}s")
        print(f"   Operation time: {operation_time_strings:.3f}s")
        print(f"   Total time: {load_time_strings + operation_time_strings:.3f}s")
        print(f"   Estimated DataFrame size: {strings_size:.1f} MB")
        
        print(f"🟢 Correct types approach:")
        print(f"   Load time: {load_time_correct:.3f}s")
        print(f"   Operation time: {operation_time_correct:.3f}s")
        print(f"   Total time: {load_time_correct + operation_time_correct:.3f}s")
        print(f"   Estimated DataFrame size: {correct_size:.1f} MB")
        
        speedup = (load_time_strings + operation_time_strings) / (load_time_correct + operation_time_correct)
        print(f"⚡ Speedup with correct types: {speedup:.2f}x")
        
        # Cleanup
        df_spark_correct.unpersist()
        self.spark.catalog.clearCache()
        
    def scenario_2_oversized_vs_rightsized_types(self):
        """Compare 64-bit types vs right-sized types"""
        print("\n🔸 SCENARIO 2: 64-bit vs Right-sized Data Types")
        print("-" * 40)
        
        # Create two different datasets to avoid schema conversion overhead
        print("Creating optimized datasets for fair comparison...")
        
        # Clear any existing cache
        self.spark.catalog.clearCache()
        
        # Create data using Spark directly to avoid pandas conversion overhead
        from pyspark.sql.functions import lit, rand, floor, when, array, expr
        
        # Generate base data in Spark
        base_df = self.spark.range(self.rows) \
            .withColumn("category_id", (floor(rand() * 100) + 1).cast("int")) \
            .withColumn("price", (rand() * 999 + 1)) \
            .withColumn("quantity", (floor(rand() * 50) + 1).cast("int")) \
            .withColumn("score", (rand() * 100)) \
            .withColumn("region_code", (floor(rand() * 10) + 1).cast("int")) \
            .withColumn("status", when(rand() < 0.33, "active")
                       .when(rand() < 0.66, "inactive")
                       .otherwise("pending")) \
            .withColumn("is_premium", (rand() < 0.5))
        
        # Scenario 2A: Everything as 64-bit (oversized)
        print("Testing: OVERSIZED 64-bit types...")
        
        # Cast to oversized types
        df_oversized = base_df.select(
            col("id").cast(LongType()).alias("id"),
            col("category_id").cast(LongType()).alias("category_id"),
            col("price").cast(DoubleType()).alias("price"),
            col("quantity").cast(LongType()).alias("quantity"),
            col("score").cast(DoubleType()).alias("score"),
            col("region_code").cast(LongType()).alias("region_code"),
            col("status"),
            col("is_premium")
        )
        
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        df_oversized.cache()
        count_oversized = df_oversized.count()  # Force materialization
        
        load_time_oversized = time.time() - start_time
        time.sleep(0.5)  # Wait for memory to stabilize
        mem_after_oversized = self.get_memory_usage()
        
        # Test complex operations
        start_time = time.time()
        result_oversized = df_oversized.groupBy("region_code", "status") \
            .agg(
                avg("price").alias("avg_price"),
                sum("quantity").alias("total_quantity"),
                count("id").alias("record_count"),
                spark_max("score").alias("max_score")
            ).collect()
        operation_time_oversized = time.time() - start_time
        
        # Scenario 2B: Right-sized data types
        print("Testing: RIGHT-SIZED data types...")
        
        # Clean up previous dataframe and clear cache
        df_oversized.unpersist()
        self.spark.catalog.clearCache()
        
        # Cast to right-sized types (using the same base data)
        df_rightsized = base_df.select(
            col("id").cast(IntegerType()).alias("id"),
            col("category_id").cast(ByteType()).alias("category_id"),
            col("price").cast(FloatType()).alias("price"),
            col("quantity").cast(ByteType()).alias("quantity"),
            col("score").cast(FloatType()).alias("score"),
            col("region_code").cast(ByteType()).alias("region_code"),
            col("status"),
            col("is_premium")
        )
        
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        df_rightsized.cache()
        count_rightsized = df_rightsized.count()  # Force materialization
        
        load_time_rightsized = time.time() - start_time
        time.sleep(0.5)  # Wait for memory to stabilize
        mem_after_rightsized = self.get_memory_usage()
        
        # Test complex operations
        start_time = time.time()
        result_rightsized = df_rightsized.groupBy("region_code", "status") \
            .agg(
                avg("price").alias("avg_price"),
                sum("quantity").alias("total_quantity"),
                count("id").alias("record_count"),
                spark_max("score").alias("max_score")
            ).collect()
        operation_time_rightsized = time.time() - start_time
        
        # Estimate DataFrame sizes for memory comparison
        oversized_size = self.estimate_dataframe_size_mb(df_oversized)
        rightsized_size = self.estimate_dataframe_size_mb(df_rightsized)
        
        # Store results
        self.results['scenario_2'] = {
            'oversized_64bit': {
                'load_time': load_time_oversized,
                'operation_time': operation_time_oversized,
                'memory_usage': oversized_size,
                'total_time': load_time_oversized + operation_time_oversized
            },
            'rightsized': {
                'load_time': load_time_rightsized,
                'operation_time': operation_time_rightsized,
                'memory_usage': rightsized_size,
                'total_time': load_time_rightsized + operation_time_rightsized
            }
        }
        
        # Print results
        print(f"🔴 Oversized 64-bit types:")
        print(f"   Load time: {load_time_oversized:.3f}s")
        print(f"   Operation time: {operation_time_oversized:.3f}s")
        print(f"   Total time: {load_time_oversized + operation_time_oversized:.3f}s")
        print(f"   Estimated DataFrame size: {oversized_size:.1f} MB")
        
        print(f"🟢 Right-sized types:")
        print(f"   Load time: {load_time_rightsized:.3f}s")
        print(f"   Operation time: {operation_time_rightsized:.3f}s")
        print(f"   Total time: {load_time_rightsized + operation_time_rightsized:.3f}s")
        print(f"   Estimated DataFrame size: {rightsized_size:.1f} MB")
        
        speedup = (load_time_oversized + operation_time_oversized) / (load_time_rightsized + operation_time_rightsized)
        if oversized_size > 0:
            memory_savings = (oversized_size - rightsized_size) / oversized_size * 100
        else:
            memory_savings = 0
        print(f"⚡ Speedup with right-sized types: {speedup:.2f}x")
        print(f"💾 Memory savings: {memory_savings:.1f}%")
        
        # Cleanup
        df_rightsized.unpersist()
        base_df.unpersist()
        self.spark.catalog.clearCache()
        
    def scenario_3_join_performance_comparison(self):
        """Test join performance with different data type strategies"""
        print("\n🔸 SCENARIO 3: Join Performance Impact")
        print("-" * 40)
        
        # Create two datasets for joining
        df1_pandas = self.create_sample_data()
        
        # Create lookup table
        lookup_data = {
            'category_id': list(range(1, 101)),
            'category_name': [f'Category_{i}' for i in range(1, 101)],
            'category_priority': np.random.randint(1, 5, 100)
        }
        df2_pandas = pd.DataFrame(lookup_data)
        
        # Test 1: String-based join (worst case)
        print("Testing: STRING-based join...")
        df1_strings = df1_pandas.copy()
        df1_strings['category_id'] = df1_strings['category_id'].astype(str)
        df2_strings = df2_pandas.copy()
        df2_strings['category_id'] = df2_strings['category_id'].astype(str)
        
        df1_spark_str = self.spark.createDataFrame(df1_strings)
        df2_spark_str = self.spark.createDataFrame(df2_strings)
        
        start_time = time.time()
        joined_str = df1_spark_str.join(df2_spark_str, "category_id", "inner")
        result_str = joined_str.count()
        join_time_str = time.time() - start_time
        
        # Test 2: Integer-based join (optimal)
        print("Testing: INTEGER-based join...")
        df1_spark_int = self.spark.createDataFrame(df1_pandas)
        df2_spark_int = self.spark.createDataFrame(df2_pandas)
        
        start_time = time.time()
        joined_int = df1_spark_int.join(df2_spark_int, "category_id", "inner")
        result_int = joined_int.count()
        join_time_int = time.time() - start_time
        
        print(f"🔴 String-based join: {join_time_str:.3f}s")
        print(f"🟢 Integer-based join: {join_time_int:.3f}s")
        print(f"⚡ Join speedup: {join_time_str / join_time_int:.2f}x")
        
        self.results['scenario_3'] = {
            'string_join_time': join_time_str,
            'integer_join_time': join_time_int,
            'join_speedup': join_time_str / join_time_int
        }
    
    def create_visualization(self):
        """Create visualizations of the performance results"""
        print("\n📊 Creating performance visualizations...")
        
        # Set up the plotting style
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            # Fallback if seaborn style is not available
            plt.style.use('default')
            sns.set_palette("husl")
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Spark Data Types Performance Comparison', fontsize=16, fontweight='bold')
        
        # Scenario 1: Strings vs Correct Types
        if 'scenario_1' in self.results:
            ax1 = axes[0, 0]
            scenarios = ['Strings', 'Correct Types']
            times = [
                self.results['scenario_1']['strings']['total_time'],
                self.results['scenario_1']['correct_types']['total_time']
            ]
            colors = ['red', 'green']
            bars1 = ax1.bar(scenarios, times, color=colors, alpha=0.7)
            ax1.set_title('Total Processing Time\n(Strings vs Correct Types)')
            ax1.set_ylabel('Time (seconds)')
            
            # Add value labels on bars
            for bar, time in zip(bars1, times):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time:.3f}s', ha='center', va='bottom')
        
        # Scenario 1: DataFrame Size Estimates
        if 'scenario_1' in self.results:
            ax2 = axes[0, 1]
            scenarios = ['Strings', 'Correct Types']
            sizes = [
                self.results['scenario_1']['strings']['memory_usage'],
                self.results['scenario_1']['correct_types']['memory_usage']
            ]
            bars2 = ax2.bar(scenarios, sizes, color=colors, alpha=0.7)
            ax2.set_title('Estimated DataFrame Size\n(Strings vs Correct Types)')
            ax2.set_ylabel('Size (MB)')
            
            # Add value labels on bars
            for bar, size in zip(bars2, sizes):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{size:.1f}MB', ha='center', va='bottom')
        
        # Scenario 2: 64-bit vs Right-sized
        if 'scenario_2' in self.results:
            ax3 = axes[1, 0]
            scenarios = ['64-bit Types', 'Right-sized Types']
            times = [
                self.results['scenario_2']['oversized_64bit']['total_time'],
                self.results['scenario_2']['rightsized']['total_time']
            ]
            colors = ['orange', 'blue']
            bars3 = ax3.bar(scenarios, times, color=colors, alpha=0.7)
            ax3.set_title('Total Processing Time\n(64-bit vs Right-sized)')
            ax3.set_ylabel('Time (seconds)')
            
            # Add value labels on bars
            for bar, time in zip(bars3, times):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time:.3f}s', ha='center', va='bottom')
        
        # Scenario 2: DataFrame Size Estimates
        if 'scenario_2' in self.results:
            ax4 = axes[1, 1]
            scenarios = ['64-bit Types', 'Right-sized Types']
            sizes = [
                self.results['scenario_2']['oversized_64bit']['memory_usage'],
                self.results['scenario_2']['rightsized']['memory_usage']
            ]
            bars4 = ax4.bar(scenarios, sizes, color=colors, alpha=0.7)
            ax4.set_title('Estimated DataFrame Size\n(64-bit vs Right-sized)')
            ax4.set_ylabel('Size (MB)')
            
            # Add value labels on bars
            for bar, size in zip(bars4, sizes):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{size:.1f}MB', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('/Users/sdevisch/repos/hello_spark/spark_data_types_performance.png', 
                    dpi=300, bbox_inches='tight')
        plt.show()
        
    def print_summary_report(self):
        """Print a comprehensive summary report"""
        print("\n" + "="*60)
        print("📋 SPARK DATA TYPES PERFORMANCE SUMMARY REPORT")
        print("="*60)
        
        if 'scenario_1' in self.results:
            s1 = self.results['scenario_1']
            speedup_1 = s1['strings']['total_time'] / s1['correct_types']['total_time']
            print(f"\n🔸 STRINGS vs CORRECT TYPES:")
            print(f"   Performance improvement: {speedup_1:.2f}x faster")
            print(f"   Time saved: {s1['strings']['total_time'] - s1['correct_types']['total_time']:.3f}s")
            print(f"   Memory difference: {s1['strings']['memory_usage'] - s1['correct_types']['memory_usage']:.1f}MB")
        
        if 'scenario_2' in self.results:
            s2 = self.results['scenario_2']
            speedup_2 = s2['oversized_64bit']['total_time'] / s2['rightsized']['total_time']
            if s2['oversized_64bit']['memory_usage'] != 0:
                memory_savings = (s2['oversized_64bit']['memory_usage'] - s2['rightsized']['memory_usage']) / s2['oversized_64bit']['memory_usage'] * 100
            else:
                memory_savings = 0
            print(f"\n🔸 64-BIT vs RIGHT-SIZED TYPES:")
            print(f"   Performance improvement: {speedup_2:.2f}x faster")
            print(f"   Time saved: {s2['oversized_64bit']['total_time'] - s2['rightsized']['total_time']:.3f}s")
            print(f"   Memory saved: {memory_savings:.1f}%")
        
        if 'scenario_3' in self.results:
            s3 = self.results['scenario_3']
            print(f"\n🔸 JOIN PERFORMANCE:")
            print(f"   Integer vs String join speedup: {s3['join_speedup']:.2f}x faster")
        
        print(f"\n💡 KEY TAKEAWAYS:")
        print(f"   • Use correct data types instead of strings for significant performance gains")
        print(f"   • Right-size your data types to save memory and improve cache efficiency")
        print(f"   • Integer joins are much faster than string joins")
        print(f"   • Type casting during operations adds unnecessary overhead")
        print(f"   • Memory efficiency directly impacts Spark's ability to cache and process data")
        
        print("\n" + "="*60)
    
    def run_all_scenarios(self):
        """Run all performance comparison scenarios"""
        print("🚀 Starting comprehensive Spark data types performance analysis...")
        
        try:
            self.scenario_1_strings_vs_correct_types()
            self.scenario_2_oversized_vs_rightsized_types()
            self.scenario_3_join_performance_comparison()
            self.create_visualization()
            self.print_summary_report()
            
        finally:
            print("\n🧹 Cleaning up Spark session...")
            self.spark.stop()

def main():
    """Main execution function"""
    demo = SparkDataTypesDemo(rows=500_000)  # Use smaller dataset for more reliable results
    demo.run_all_scenarios()

if __name__ == "__main__":
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/09_spark_data_types_performance.md",
            title="Performance: Data types and efficiency",
            main_callable=main,
        )
    else:
        main()

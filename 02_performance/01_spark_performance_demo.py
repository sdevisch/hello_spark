#!/usr/bin/env python3
"""
Spark Performance Demo: I/O and Serialization Issues & Solutions
================================================================

This script demonstrates common performance bottlenecks in PySpark related to:
1. I/O Operations (file formats, partitioning, caching)
2. Serialization Issues (Python UDFs vs native functions)
3. Data Movement (shuffling, broadcasting)
4. Memory Management (persistence strategies)

Each section shows the SLOW approach followed by the FAST solution.
"""

import time
import random
import tempfile
import shutil
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import StorageLevel
import pyspark.sql.functions as F

class PerformanceBenchmark:
    def __init__(self, app_name="SparkPerformanceDemo"):
        """Initialize Spark session with performance optimizations"""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master("local[*]") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")  # Reduce log noise
        
        # Create temp directory for demo files
        self.temp_dir = Path(tempfile.mkdtemp())
        print(f"📁 Temp directory: {self.temp_dir}")
        print(f"🌐 Spark UI: http://localhost:4040")
        print("=" * 60)

    def time_operation(self, operation_name, func, *args, **kwargs):
        """Time a Spark operation and return results with timing"""
        print(f"\n⏱️  Timing: {operation_name}")
        start_time = time.time()
        result = func(*args, **kwargs)
        
        # Force action to ensure computation happens
        if hasattr(result, 'count'):
            count = result.count()
            end_time = time.time()
            duration = end_time - start_time
            print(f"   ✅ Completed in {duration:.2f}s (processed {count:,} rows)")
        else:
            end_time = time.time()
            duration = end_time - start_time
            print(f"   ✅ Completed in {duration:.2f}s")
        
        return result, duration

    def generate_sample_data(self, num_rows=1000000):
        """Generate sample data for demonstrations"""
        print(f"\n📊 Generating {num_rows:,} rows of sample data...")
        
        # Generate data using Spark (more efficient than Python lists for large data)
        df = self.spark.range(num_rows).select(
            col("id"),
            (rand() * 100).cast("int").alias("score"),
            (rand() * 1000).cast("int").alias("value"),
            when(rand() > 0.5, "A").otherwise("B").alias("category"),
            date_sub(current_date(), (rand() * 30).cast("int")).alias("date"),
            concat(lit("user_"), col("id")).alias("user_id")
        )
        
        return df

    def demo_1_file_format_performance(self):
        """Demonstrate file format performance differences"""
        print("\n" + "="*60)
        print("🗂️  DEMO 1: FILE FORMAT PERFORMANCE")
        print("="*60)
        
        df = self.generate_sample_data(100000)
        
        # SLOW: CSV format (text-based, no compression, no schema)
        csv_path = self.temp_dir / "data.csv"
        
        _, csv_write_time = self.time_operation(
            "SLOW - Writing CSV", 
            lambda: df.write.mode("overwrite").csv(str(csv_path))
        )
        
        _, csv_read_time = self.time_operation(
            "SLOW - Reading CSV", 
            lambda: self.spark.read.csv(str(csv_path), header=True, inferSchema=True)
        )
        
        # FAST: Parquet format (columnar, compressed, schema preserved)
        parquet_path = self.temp_dir / "data.parquet"
        
        _, parquet_write_time = self.time_operation(
            "FAST - Writing Parquet", 
            lambda: df.write.mode("overwrite").parquet(str(parquet_path))
        )
        
        _, parquet_read_time = self.time_operation(
            "FAST - Reading Parquet", 
            lambda: self.spark.read.parquet(str(parquet_path))
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   CSV Total Time:     {csv_write_time + csv_read_time:.2f}s")
        print(f"   Parquet Total Time: {parquet_write_time + parquet_read_time:.2f}s")
        print(f"   Speedup: {(csv_write_time + csv_read_time)/(parquet_write_time + parquet_read_time):.1f}x faster")

    def demo_2_serialization_issues(self):
        """Demonstrate Python UDF vs native function performance"""
        print("\n" + "="*60)
        print("🐍 DEMO 2: SERIALIZATION ISSUES (Python UDFs)")
        print("="*60)
        
        df = self.generate_sample_data(500000)
        
        # SLOW: Python UDF (requires serialization between JVM and Python)
        def slow_python_udf(value):
            """Slow Python function that gets serialized"""
            return value * 2 + 10
        
        from pyspark.sql.functions import udf
        slow_udf = udf(slow_python_udf, IntegerType())
        
        _, slow_time = self.time_operation(
            "SLOW - Python UDF with serialization",
            lambda: df.select("*", slow_udf(col("score")).alias("transformed_score"))
        )
        
        # FAST: Native Spark functions (no serialization, runs in JVM)
        _, fast_time = self.time_operation(
            "FAST - Native Spark functions",
            lambda: df.select("*", (col("score") * 2 + 10).alias("transformed_score"))
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   Python UDF Time:    {slow_time:.2f}s")
        print(f"   Native Spark Time:  {fast_time:.2f}s")
        print(f"   Speedup: {slow_time/fast_time:.1f}x faster")
        print(f"   💡 Tip: Use built-in Spark functions instead of Python UDFs!")

    def demo_3_caching_strategies(self):
        """Demonstrate caching and persistence strategies"""
        print("\n" + "="*60)
        print("💾 DEMO 3: CACHING AND PERSISTENCE STRATEGIES")
        print("="*60)
        
        df = self.generate_sample_data(800000)
        
        # Create a complex transformation that we'll reuse
        complex_df = df.filter(col("score") > 50) \
                      .groupBy("category") \
                      .agg(avg("score").alias("avg_score"),
                           count("*").alias("count"),
                           max("value").alias("max_value"))
        
        # SLOW: Recomputing the same transformation multiple times
        print("\n🐌 SLOW: No caching - recomputing transformations")
        
        _, slow_time1 = self.time_operation(
            "SLOW - First computation (no cache)",
            lambda: complex_df.filter(col("avg_score") > 60)
        )
        
        _, slow_time2 = self.time_operation(
            "SLOW - Second computation (no cache)",
            lambda: complex_df.filter(col("count") > 100000)
        )
        
        # FAST: Cache the intermediate result
        print("\n🚀 FAST: With caching - compute once, reuse multiple times")
        
        cached_df = complex_df.cache()
        
        _, fast_time1 = self.time_operation(
            "FAST - First computation (with cache)",
            lambda: cached_df.filter(col("avg_score") > 60)
        )
        
        _, fast_time2 = self.time_operation(
            "FAST - Second computation (from cache)",
            lambda: cached_df.filter(col("count") > 100000)
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   No Cache Total Time:   {slow_time1 + slow_time2:.2f}s")
        print(f"   With Cache Total Time: {fast_time1 + fast_time2:.2f}s")
        print(f"   Speedup: {(slow_time1 + slow_time2)/(fast_time1 + fast_time2):.1f}x faster")
        print(f"   💡 Tip: Cache DataFrames that are used multiple times!")

    def demo_4_partitioning_strategies(self):
        """Demonstrate partitioning impact on performance"""
        print("\n" + "="*60)
        print("🗂️  DEMO 4: PARTITIONING STRATEGIES")
        print("="*60)
        
        df = self.generate_sample_data(1000000)
        
        # SLOW: Too many small partitions
        print("\n🐌 SLOW: Too many small partitions")
        over_partitioned = df.repartition(1000)  # Way too many partitions
        
        _, slow_time = self.time_operation(
            "SLOW - Over-partitioned aggregation",
            lambda: over_partitioned.groupBy("category").agg(
                avg("score").alias("avg_score"),
                count("*").alias("count")
            )
        )
        
        # FAST: Optimal partitioning (rule of thumb: 2-3 partitions per CPU core)
        print("\n🚀 FAST: Optimal partitioning")
        optimal_partitions = 8  # For local[*] with typical laptop
        well_partitioned = df.repartition(optimal_partitions)
        
        _, fast_time = self.time_operation(
            "FAST - Optimally partitioned aggregation",
            lambda: well_partitioned.groupBy("category").agg(
                avg("score").alias("avg_score"),
                count("*").alias("count")
            )
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   Over-partitioned Time:  {slow_time:.2f}s")
        print(f"   Optimal partition Time: {fast_time:.2f}s")
        print(f"   Speedup: {slow_time/fast_time:.1f}x faster")
        print(f"   💡 Tip: Use 2-3 partitions per CPU core for optimal performance!")

    def demo_5_broadcast_vs_shuffle(self):
        """Demonstrate broadcast join vs shuffle join performance"""
        print("\n" + "="*60)
        print("📡 DEMO 5: BROADCAST VS SHUFFLE JOINS")
        print("="*60)
        
        # Large dataset
        large_df = self.generate_sample_data(500000)
        
        # Small lookup table (perfect for broadcasting)
        small_df = self.spark.createDataFrame([
            ("A", "Category Alpha", 1.5),
            ("B", "Category Beta", 2.0)
        ], ["category", "category_name", "multiplier"])
        
        print(f"📊 Large dataset: {large_df.count():,} rows")
        print(f"📊 Small dataset: {small_df.count():,} rows")
        
        # SLOW: Regular join (causes shuffle of large dataset)
        print("\n🐌 SLOW: Regular join (shuffle)")
        
        _, slow_time = self.time_operation(
            "SLOW - Shuffle join",
            lambda: large_df.join(small_df, "category").select(
                "id", "score", "category_name", 
                (col("score") * col("multiplier")).alias("adjusted_score")
            )
        )
        
        # FAST: Broadcast join (small table broadcasted to all nodes)
        print("\n🚀 FAST: Broadcast join")
        
        _, fast_time = self.time_operation(
            "FAST - Broadcast join",
            lambda: large_df.join(broadcast(small_df), "category").select(
                "id", "score", "category_name", 
                (col("score") * col("multiplier")).alias("adjusted_score")
            )
        )
        
        print(f"\n📈 RESULTS:")
        print(f"   Shuffle Join Time:   {slow_time:.2f}s")
        print(f"   Broadcast Join Time: {fast_time:.2f}s")
        print(f"   Speedup: {slow_time/fast_time:.1f}x faster")
        print(f"   💡 Tip: Broadcast small tables (< 10MB) to avoid shuffles!")

    def demo_6_memory_management(self):
        """Demonstrate different persistence strategies"""
        print("\n" + "="*60)
        print("🧠 DEMO 6: MEMORY MANAGEMENT & PERSISTENCE")
        print("="*60)
        
        df = self.generate_sample_data(300000)
        
        # Test different storage levels (avoid *_SER variants for compatibility)
        storage_levels = [
            ("MEMORY_ONLY", StorageLevel.MEMORY_ONLY),
            ("MEMORY_AND_DISK", StorageLevel.MEMORY_AND_DISK),
            ("DISK_ONLY", StorageLevel.DISK_ONLY)
        ]
        
        results = {}
        
        for name, level in storage_levels:
            print(f"\n🧪 Testing {name} persistence:")
            
            # Create a transformation that will benefit from caching
            complex_df = df.filter(col("score") > 30) \
                          .withColumn("complex_calc", 
                                    col("score") * col("value") / 100) \
                          .persist(level)
            
            # Force caching by triggering an action
            _, cache_time = self.time_operation(
                f"{name} - Initial caching",
                lambda: complex_df.count()
            )
            
            # Test access speed from cache
            _, access_time = self.time_operation(
                f"{name} - Access from cache",
                lambda: complex_df.filter(col("complex_calc") > 500).count()
            )
            
            results[name] = {"cache_time": cache_time, "access_time": access_time}
            
            # Unpersist to free memory for next test
            complex_df.unpersist()
        
        print(f"\n📈 PERSISTENCE STRATEGY COMPARISON:")
        print(f"{'Strategy':<20} {'Cache Time':<12} {'Access Time':<12} {'Total':<10}")
        print("-" * 60)
        
        for name, times in results.items():
            total = times["cache_time"] + times["access_time"]
            print(f"{name:<20} {times['cache_time']:<12.2f} {times['access_time']:<12.2f} {total:<10.2f}")
        
        print(f"\n💡 Tips:")
        print(f"   - MEMORY_ONLY: Fastest but may cause OOM")
        print(f"   - MEMORY_AND_DISK: Good balance (recommended)")
        # SERIALIZED variants omitted for cross-version compatibility
        print(f"   - DISK_ONLY: Slowest but handles large datasets")

    def run_all_demos(self):
        """Run all performance demonstrations"""
        print("🚀 SPARK PERFORMANCE DEMONSTRATION")
        print("=" * 60)
        print("This demo will show common performance bottlenecks and solutions")
        print("Watch the Spark UI at http://localhost:4040 for detailed metrics!")
        
        try:
            self.demo_1_file_format_performance()
            self.demo_2_serialization_issues()
            self.demo_3_caching_strategies()
            self.demo_4_partitioning_strategies()
            self.demo_5_broadcast_vs_shuffle()
            self.demo_6_memory_management()
            
            print("\n" + "="*60)
            print("🎉 ALL DEMOS COMPLETED!")
            print("="*60)
            print("\n🎯 KEY TAKEAWAYS:")
            print("1. 📁 Use Parquet instead of CSV for better I/O performance")
            print("2. 🐍 Avoid Python UDFs - use native Spark functions")
            print("3. 💾 Cache DataFrames that are accessed multiple times")
            print("4. 🗂️  Use optimal partitioning (2-3 partitions per CPU core)")
            print("5. 📡 Broadcast small tables to avoid expensive shuffles")
            print("6. 🧠 Choose appropriate persistence strategy for your use case")
            
            print(f"\n🌐 Spark UI: http://localhost:4040")
            print("   Check the 'SQL' and 'Jobs' tabs to see execution plans!")
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
        finally:
            # Reduce/skip wait when generating docs
            import os as _os
            if _os.environ.get("GENERATE_DOCS", "0") == "1":
                print("\n⏳ Skipping 60s keep-alive for docs generation")
            else:
                print(f"\n⏳ Keeping Spark session alive for 60 seconds...")
                print("   Explore the Spark UI to see detailed execution metrics!")
                print("   Press Ctrl+C to stop early.")
                try:
                    time.sleep(60)
                except KeyboardInterrupt:
                    print("\n🛑 Interrupted by user")
            
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        
        # Remove temp directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"   ✅ Removed temp directory: {self.temp_dir}")
        
        # Stop Spark session
        self.spark.stop()
        print("   ✅ Stopped Spark session")
        print("\n👋 Demo completed!")


def main():
    """Main function to run the performance demonstration"""
    print("🚀 Starting Spark Performance Demo...")
    print("📚 Docs index: docs/index.md")
    
    benchmark = PerformanceBenchmark()
    benchmark.run_all_demos()


if __name__ == "__main__":
    import os as _os
    if _os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/perf_01_spark_performance_demo.md",
            title="Performance 01: I/O, serialization, caching, partitions, joins, persistence",
            main_callable=main,
        )
    else:
        main()

#!/usr/bin/env python3
"""
Conclusion first: Serialization is visible—find it and avoid it
===============================================================

Conclusion: Prefer native Spark functions and look for 'BatchEvalPython' in
execution plans. That is where data crosses JVM↔Python and slows down.

Why: Python UDFs require serialization and add overhead; native expressions run
entirely in the JVM. The UI and `explain()` make this visible.

What: Show how to spot and time serialization hotspots.

How: Use `explain()`, compare native vs UDF, and watch the SQL tab in the UI.
"""

import time
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

class SerializationObserver:
    def __init__(self):
        """Initialize Spark session with detailed logging"""
        print("🔍 OBSERVING SERIALIZATION IN SPARK")
        print("=" * 50)
        
        # Create Spark session with detailed execution info
        self.spark = SparkSession.builder \
            .appName("SerializationObserver") \
            .master("local[*]") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .config("spark.sql.adaptive.enabled", "false") \
            .getOrCreate()
        
        # Set log level to see more details
        self.spark.sparkContext.setLogLevel("WARN")
        
        print(f"🌐 Spark UI: http://localhost:4040")
        print("=" * 50)

    def create_sample_data(self, size=100000):
        """Create simple sample data for demonstrations"""
        print(f"📊 Creating {size:,} rows of sample data...")
        
        df = self.spark.range(size).select(
            col("id"),
            (rand() * 100).cast("int").alias("value"),
            when(col("id") % 2 == 0, "even").otherwise("odd").alias("category")
        )
        
        return df

    def demo_1_basic_explain(self):
        """Demonstrate basic explain() usage"""
        print("\n" + "="*50)
        print("📋 DEMO 1: BASIC EXPLAIN() USAGE")
        print("="*50)
        
        df = self.create_sample_data(50000)
        
        print("\n🔍 1. Simple transformation (no UDF):")
        simple_df = df.select("id", (col("value") * 2).alias("doubled"))
        print("\n📊 Execution Plan:")
        simple_df.explain(True)  # Show all execution plan details
        
        print("\n" + "-"*50)
        print("🔍 2. With aggregation:")
        agg_df = df.groupBy("category").agg(avg("value").alias("avg_value"))
        print("\n📊 Execution Plan:")
        agg_df.explain(True)
        
        print("\n💡 KEY OBSERVATIONS:")
        print("   - Notice the plan shows only Catalyst operations")
        print("   - No mention of Python or serialization")
        print("   - All operations happen in the JVM")

    def demo_2_udf_in_execution_plan(self):
        """Show how UDFs appear in execution plans"""
        print("\n" + "="*50)
        print("🐍 DEMO 2: UDF IN EXECUTION PLANS")
        print("="*50)
        
        df = self.create_sample_data(50000)
        
        # Define a simple Python UDF
        def python_double(value):
            """Simple Python function that doubles a value"""
            return value * 2
        
        double_udf = udf(python_double, IntegerType())
        
        print("\n🔍 Native Spark function execution plan:")
        native_df = df.select("id", (col("value") * 2).alias("doubled"))
        native_df.explain(True)
        
        print("\n" + "-"*50)
        print("🔍 Python UDF execution plan:")
        udf_df = df.select("id", double_udf("value").alias("doubled"))
        udf_df.explain(True)
        
        print("\n💡 KEY OBSERVATIONS:")
        print("   - UDF plans show 'BatchEvalPython' or similar")
        print("   - This indicates data serialization to Python")
        print("   - Much more complex execution plan")
        print("   - Serialization happens at the BatchEvalPython stage")

    def demo_3_timing_with_explain(self):
        """Demonstrate timing differences with explain analysis"""
        print("\n" + "="*50)
        print("⏱️  DEMO 3: TIMING WITH EXPLAIN ANALYSIS") 
        print("="*50)
        
        df = self.create_sample_data(100000)
        
        # Define UDF for comparison
        def complex_calc(value):
            """Slightly more complex calculation"""
            import math
            return int(math.sqrt(value) * 2)
        
        calc_udf = udf(complex_calc, IntegerType())
        
        # Native Spark version
        native_df = df.select("id", sqrt(col("value")).cast("int").alias("result"))
        
        # UDF version  
        udf_df = df.select("id", calc_udf("value").alias("result"))
        
        print("\n🚀 1. Native Spark function:")
        print("   Execution plan with timing:")
        
        start_time = time.time()
        native_count = native_df.count()
        native_time = time.time() - start_time
        
        print(f"   ✅ Processed {native_count:,} rows in {native_time:.3f}s")
        native_df.explain("formatted")  # Show formatted execution plan
        
        print("\n🐍 2. Python UDF:")
        print("   Execution plan with timing:")
        
        start_time = time.time()
        udf_count = udf_df.count()
        udf_time = time.time() - start_time
        
        print(f"   ✅ Processed {udf_count:,} rows in {udf_time:.3f}s")
        udf_df.explain("formatted")
        
        print(f"\n📈 PERFORMANCE COMPARISON:")
        print(f"   Native Spark: {native_time:.3f}s")
        print(f"   Python UDF:   {udf_time:.3f}s")
        print(f"   Speedup:      {udf_time/native_time:.1f}x faster with native")

    def demo_4_identifying_serialization_points(self):
        """Show how to identify serialization points in complex queries"""
        print("\n" + "="*50)
        print("🎯 DEMO 4: IDENTIFYING SERIALIZATION POINTS")
        print("="*50)
        
        df = self.create_sample_data(80000)
        
        # Create a complex query mixing native and UDF operations
        def categorize_value(value):
            """Python function to categorize values"""
            if value < 25:
                return "low"
            elif value < 75:
                return "medium"
            else:
                return "high"
        
        categorize_udf = udf(categorize_value, StringType())
        
        print("\n🔍 Complex query with mixed operations:")
        
        complex_df = df \
            .filter(col("value") > 10) \
            .select("id", "value", categorize_udf("value").alias("category_python")) \
            .withColumn("value_squared", col("value") * col("value")) \
            .groupBy("category_python") \
            .agg(
                avg("value").alias("avg_value"),
                avg("value_squared").alias("avg_squared"),
                count("*").alias("count")
            )
        
        print("\n📊 Full execution plan:")
        complex_df.explain("extended")
        
        # Force execution and time it
        start_time = time.time()
        result = complex_df.collect()
        execution_time = time.time() - start_time
        
        print(f"\n⏱️  Execution time: {execution_time:.3f}s")
        print("\n🔍 Results:")
        for row in result:
            print(f"   {row}")
        
        print("\n💡 SERIALIZATION IDENTIFICATION:")
        print("   1. Look for 'BatchEvalPython' in the plan")
        print("   2. This shows exactly where Python UDF runs")
        print("   3. Data flows: JVM → Python → JVM at this point")
        print("   4. All operations before/after are pure Spark")

    def demo_5_spark_ui_observation(self):
        """Show how to use Spark UI to observe serialization"""
        print("\n" + "="*50)
        print("🌐 DEMO 5: SPARK UI OBSERVATION")
        print("="*50)
        
        df = self.create_sample_data(150000)
        
        def expensive_python_func(value):
            """Deliberately expensive Python function"""
            total = 0
            for i in range(int(value) % 10 + 1):
                total += i * 2
            return total
        
        expensive_udf = udf(expensive_python_func, IntegerType())
        
        print("\n🚀 Running operation with UDF...")
        print("   👀 Open Spark UI: http://localhost:4040")
        print("   📊 Go to 'SQL' tab to see query details")
        print("   🔍 Look for stages with 'Python' in the description")
        
        # Run the operation
        result_df = df.select("id", expensive_udf("value").alias("expensive_result"))
        
        start_time = time.time()
        count = result_df.count()
        execution_time = time.time() - start_time
        
        print(f"\n✅ Processed {count:,} rows in {execution_time:.3f}s")
        print("\n🔍 WHAT TO LOOK FOR IN SPARK UI:")
        print("   1. 'SQL' tab → Click on the query")
        print("   2. Look for stages with 'BatchEvalPython'")
        print("   3. These stages show serialization overhead")
        print("   4. Compare timing with pure Spark stages")
        print("   5. 'Details' show the full execution plan")

    def demo_6_simple_diagnostic_tools(self):
        """Show simple tools to diagnose serialization issues"""
        print("\n" + "="*50)
        print("🛠️  DEMO 6: SIMPLE DIAGNOSTIC TOOLS")
        print("="*50)
        
        df = self.create_sample_data(100000)
        
        print("\n📊 Tool 1: explain('cost') - shows cost-based optimization:")
        simple_query = df.filter(col("value") > 50).select("id", "value")
        simple_query.explain("cost")
        
        print("\n📊 Tool 2: show() vs collect() performance:")
        
        # UDF that we'll test
        def double_value(x):
            return x * 2
        
        double_udf = udf(double_value, IntegerType())
        test_df = df.select("id", double_udf("value").alias("doubled")).limit(10)
        
        # Time show() - only materializes what's displayed
        start = time.time()
        print("   show() output:")
        test_df.show(5)
        show_time = time.time() - start
        
        # Time collect() - materializes everything
        start = time.time()
        collected = test_df.collect()
        collect_time = time.time() - start
        
        print(f"\n⏱️  show() time: {show_time:.3f}s")
        print(f"   collect() time: {collect_time:.3f}s")
        
        print("\n📊 Tool 3: Cache impact on UDF performance:")
        cached_df = test_df.cache()
        
        # First access (cache miss)
        start = time.time()
        cached_df.count()
        first_access = time.time() - start
        
        # Second access (cache hit)
        start = time.time()
        cached_df.count()
        second_access = time.time() - start
        
        print(f"   First access (cache miss): {first_access:.3f}s")
        print(f"   Second access (cache hit): {second_access:.3f}s")
        print(f"   Cache speedup: {first_access/second_access:.1f}x")

    def run_all_demos(self):
        """Run all serialization observation demonstrations"""
        try:
            self.demo_1_basic_explain()
            self.demo_2_udf_in_execution_plan()
            self.demo_3_timing_with_explain()
            self.demo_4_identifying_serialization_points()
            self.demo_5_spark_ui_observation()
            self.demo_6_simple_diagnostic_tools()
            
            print("\n" + "="*50)
            print("🎉 ALL SERIALIZATION OBSERVATION DEMOS COMPLETED!")
            print("="*50)
            
            print("\n🎯 KEY TAKEAWAYS FOR OBSERVING SERIALIZATION:")
            print("1. 🔍 Use explain() to see execution plans")
            print("2. 👀 Look for 'BatchEvalPython' in plans (= serialization)")
            print("3. ⏱️  Time operations to measure serialization overhead")
            print("4. 🌐 Use Spark UI SQL tab to see detailed query execution")
            print("5. 🛠️  Use explain('formatted') for readable plans")
            print("6. 📊 Compare native vs UDF execution plans side-by-side")
            
            print(f"\n🌐 Keep exploring: http://localhost:4040")
            print("   Go to SQL tab → Click queries → See execution details")
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
        finally:
            # Skip long waits when generating docs
            if os.environ.get("GENERATE_DOCS", "0") == "1":
                print("\n⏳ Skipping 30s keep-alive for docs generation")
            else:
                print(f"\n⏳ Keeping Spark session alive for 30 seconds...")
                print("   Perfect time to explore the Spark UI!")
                try:
                    time.sleep(30)
                except KeyboardInterrupt:
                    print("\n🛑 Interrupted by user")
            
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print(f"\n🧹 Cleaning up...")
        self.spark.stop()
        print("   ✅ Stopped Spark session")
        print("\n👋 Serialization observation demo completed!")


def main():
    """Main function to run the serialization observation demo"""
    print("🔍 Starting Serialization Observation Demo...")
    print("📚 Docs index: docs/index.md")
    
    observer = SerializationObserver()
    observer.run_all_demos()


if __name__ == "__main__":
    if os.environ.get("GENERATE_DOCS", "0") == "1":
        import sys as _sys, os as _os
        ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
        if ROOT not in _sys.path:
            _sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/ser_00_observe_serialization.md",
            title="Serialization 00: Using explain() and diagnostics",
            main_callable=main,
        )
    else:
        main()

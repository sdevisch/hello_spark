#!/usr/bin/env python3
"""
Simple Spark UI Demo - keeps a Spark session running for UI exploration
Run this script and access the Spark UI at http://localhost:4040
"""

from pyspark.sql import SparkSession
import time
import signal
import sys
import os

GENERATE_DOCS = os.environ.get("GENERATE_DOCS", "0") == "1"

def signal_handler(sig, frame):
    print('\n🛑 Received interrupt signal. Stopping Spark session...')
    if 'spark' in globals():
        spark.stop()
        print('✅ Spark session stopped successfully!')
    sys.exit(0)

def main():
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Starting Spark session for UI exploration...")
    
    # Initialize Spark Session with some sample data processing
    spark = SparkSession.builder \
        .appName("SparkUI-Demo") \
        .master("local[*]") \
        .config("spark.ui.port", "4040") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    print("=" * 60)
    print("🎉 Spark Session Started Successfully!")
    print(f"🌐 Spark UI: http://localhost:4040")
    print(f"🆔 Application ID: {spark.sparkContext.applicationId}")
    print(f"📊 Spark Version: {spark.version}")
    print("=" * 60)
    
    # Create some sample jobs to show in the UI
    print("📊 Creating sample jobs for UI demonstration...")
    
    # Job 1: Simple RDD operations
    print("  • Running Job 1: RDD Operations")
    rdd = spark.sparkContext.parallelize(range(1, 1001), 8)
    squares = rdd.map(lambda x: x * x)
    result1 = squares.filter(lambda x: x % 2 == 0).count()
    print(f"    Result: {result1} even squares")
    
    # Job 2: DataFrame operations
    print("  • Running Job 2: DataFrame Operations")
    df = spark.range(1, 10001).toDF("number")
    df = df.withColumn("square", df.number * df.number)
    df = df.withColumn("is_even", df.square % 2 == 0)
    result2 = df.filter(df.is_even).count()
    print(f"    Result: {result2} even squares in DataFrame")
    
    # Job 3: SQL operations
    print("  • Running Job 3: SQL Operations")
    df.createOrReplaceTempView("numbers")
    result3 = spark.sql("""
        SELECT 
            COUNT(*) as total_count,
            AVG(square) as avg_square,
            MAX(square) as max_square
        FROM numbers 
        WHERE is_even = true
    """).collect()[0]
    print(f"    Result: Total={result3['total_count']}, Avg={result3['avg_square']:.2f}, Max={result3['max_square']}")
    
    print("\n🎯 Sample jobs completed! Now you can explore the Spark UI:")
    print("   📋 Jobs Tab: See the 3 jobs we just ran")
    print("   📊 Stages Tab: View task execution details")
    print("   🔧 SQL Tab: Check the SQL query execution plan")
    print("   ⚙️  Environment Tab: View Spark configuration")
    print("   💻 Executors Tab: Monitor resource usage")
    
    print(f"\n⏰ Keeping session alive indefinitely...")
    print("💡 Press Ctrl+C to stop when you're done exploring")
    print("🌐 Spark UI: http://localhost:4040")
    
    # Keep-alive loop; shorten or skip when generating docs
    if GENERATE_DOCS:
        print("⏳ Skipping long keep-alive for docs generation")
    else:
        try:
            while True:
                time.sleep(60)
                print(f"⏳ Session still active - UI available at http://localhost:4040")
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    if GENERATE_DOCS:
        ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
        from utils.docgen import run_and_save_markdown

        run_and_save_markdown(
            markdown_path="docs/generated/02_ui_output.md",
            title="Spark UI Demo: Sample jobs and UI exploration",
            main_callable=main,
        )
    else:
        main()

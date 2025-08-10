#!/usr/bin/env python3
"""
Hello World example using Apache Spark (PySpark) with extended UI access
This script demonstrates basic Spark operations and keeps the session alive
so you can access the Spark UI at http://localhost:4040
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import time
import sys

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("HelloWorldSpark-WithUI") \
        .master("local[*]") \
        .config("spark.ui.port", "4040") \
        .getOrCreate()
    
    # Get Spark Context from the session
    sc = spark.sparkContext
    
    print("=" * 50)
    print("Hello World with Apache Spark!")
    print("=" * 50)
    print(f"🌐 Spark UI is available at: http://localhost:4040")
    print(f"📊 Application ID: {sc.applicationId}")
    print("=" * 50)
    
    # Example 1: Basic RDD operations
    print("\n1. Basic RDD Operations:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rdd = sc.parallelize(data)
    
    # Transformations
    squared_rdd = rdd.map(lambda x: x * x)
    even_rdd = rdd.filter(lambda x: x % 2 == 0)
    
    # Actions
    print(f"Original data: {rdd.collect()}")
    print(f"Squared numbers: {squared_rdd.collect()}")
    print(f"Even numbers: {even_rdd.collect()}")
    print(f"Sum of all numbers: {rdd.sum()}")
    print(f"Count: {rdd.count()}")
    
    # Example 2: Working with text data
    print("\n2. Text Processing:")
    text_data = ["Hello World", "Apache Spark", "Big Data Processing", "Distributed Computing"]
    text_rdd = sc.parallelize(text_data)
    
    # Word count example
    words_rdd = text_rdd.flatMap(lambda line: line.split(" "))
    word_pairs_rdd = words_rdd.map(lambda word: (word.lower(), 1))
    word_counts = word_pairs_rdd.reduceByKey(lambda a, b: a + b)
    
    print(f"Text data: {text_data}")
    print(f"Word counts: {dict(word_counts.collect())}")
    
    # Example 3: Using DataFrame API (Spark SQL)
    print("\n3. DataFrame Operations:")
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType
    
    # Create a DataFrame
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("city", StringType(), True)
    ])
    
    people_data = [
        ("Alice", 25, "New York"),
        ("Bob", 30, "San Francisco"),
        ("Charlie", 35, "Seattle"),
        ("Diana", 28, "Boston")
    ]
    
    df = spark.createDataFrame(people_data, schema)
    
    print("People DataFrame:")
    df.show()
    
    print("People older than 27:")
    df.filter(df.age > 27).show()
    
    print("Average age:")
    df.agg({"age": "avg"}).show()
    
    # Example 4: SQL queries
    print("\n4. SQL Queries:")
    df.createOrReplaceTempView("people")
    
    result = spark.sql("SELECT city, COUNT(*) as count FROM people GROUP BY city ORDER BY count DESC")
    print("People count by city:")
    result.show()
    
    # Example 5: Keep session alive for UI exploration
    print("\n" + "=" * 60)
    print("🎉 Spark Hello World completed successfully!")
    print(f"📊 Spark Version: {spark.version}")
    print(f"🌐 Spark UI: http://localhost:4040")
    print(f"🆔 Application ID: {sc.applicationId}")
    print("=" * 60)
    
    print(f"\n⏰ Keeping Spark session alive for 5 minutes...")
    print("📱 You can now access the Spark UI in your browser!")
    print("🔍 Check the following tabs in the UI:")
    print("   • Jobs: View completed and running jobs")
    print("   • Stages: See task execution details")
    print("   • Storage: Check cached/persisted data")
    print("   • Environment: View Spark configuration")
    print("   • Executors: Monitor resource usage")
    print("\n💡 Press Ctrl+C to stop the application early")
    
    try:
        # Keep the session alive for 5 minutes (300 seconds)
        for i in range(300, 0, -30):
            print(f"⏳ Time remaining: {i//60}:{i%60:02d} minutes")
            time.sleep(30)
        
        print("⏰ Time's up! Stopping Spark session...")
        
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal. Stopping Spark session...")
    
    finally:
        # Stop the Spark session
        spark.stop()
        print("✅ Spark session stopped successfully!")

if __name__ == "__main__":
    main()

# Hello World with Apache Spark

This repository contains Hello World examples for Apache Spark in both Python (PySpark) and Scala. These examples demonstrate basic Spark operations including RDD transformations, actions, DataFrame operations, and SQL queries.

## Prerequisites

### For Python (PySpark)
- Python 3.8 or higher
- Java 8 or 11 (required by Spark)

### For Scala
- Java 8 or 11
- Scala 2.12.x
- SBT (Scala Build Tool)

## Installation & Setup

### Python Setup

1. **Install Java** (if not already installed):
   ```bash
   # On macOS with Homebrew
   brew install openjdk@11
   
   # On Ubuntu/Debian
   sudo apt-get install openjdk-11-jdk
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Python example**:
   ```bash
   python hello_world_python.py
   ```

### Scala Setup

1. **Install SBT** (if not already installed):
   ```bash
   # On macOS with Homebrew
   brew install sbt
   
   # On Ubuntu/Debian
   echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
   curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
   sudo apt-get update
   sudo apt-get install sbt
   ```

2. **Compile and run the Scala example**:
   ```bash
   # Option 1: Run directly with SBT
   sbt "runMain HelloWorldSpark"
   
   # Option 2: Create a JAR and run with spark-submit
   sbt assembly
   spark-submit target/scala-2.12/HelloWorldSpark-assembly-1.0.jar
   ```

## What the Examples Demonstrate

Both examples showcase the following Spark concepts:

1. **Basic RDD Operations**
   - Creating RDDs from collections
   - Transformations (map, filter)
   - Actions (collect, sum, count)

2. **Text Processing**
   - Word count using flatMap, map, and reduceByKey
   - Working with string data

3. **DataFrame Operations**
   - Creating DataFrames with schema
   - Filtering and aggregations
   - Structured data processing

4. **SQL Queries**
   - Creating temporary views
   - Running SQL queries on DataFrames

5. **Functional Programming** (Scala example)
   - Chaining operations
   - Immutable data transformations

## Expected Output

When you run either example, you should see output similar to:

```
==================================================
Hello World with Apache Spark!
==================================================

1. Basic RDD Operations:
Original data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Squared numbers: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
Even numbers: [2, 4, 6, 8, 10]
Sum of all numbers: 55
Count: 10

2. Text Processing:
Text data: [Hello World, Apache Spark, Big Data Processing, Distributed Computing]
Word counts: {hello: 1, world: 1, apache: 1, spark: 1, big: 1, data: 2, processing: 1, distributed: 1, computing: 1}

3. DataFrame Operations:
People DataFrame:
+-------+---+-------------+
|   name|age|         city|
+-------+---+-------------+
|  Alice| 25|     New York|
|    Bob| 30|San Francisco|
|Charlie| 35|      Seattle|
|  Diana| 28|       Boston|
+-------+---+-------------+

...
```

## Monitoring

While the examples are running, you can access the Spark UI at:
- **Local Spark UI**: http://localhost:4040

This provides insights into job execution, stages, and performance metrics.

## Next Steps

After running these examples, you might want to explore:

1. **Reading from files**: Load CSV, JSON, or Parquet files
2. **Writing output**: Save results to various formats
3. **Advanced transformations**: joins, window functions, user-defined functions
4. **Streaming**: Real-time data processing with Spark Streaming
5. **Machine Learning**: MLlib for distributed machine learning

## Troubleshooting

### Common Issues

1. **Java not found**: Ensure Java 8 or 11 is installed and JAVA_HOME is set
2. **Permission errors**: Make sure you have write permissions in the directory
3. **Port conflicts**: If port 4040 is busy, Spark will use the next available port

### Environment Variables

You may need to set these environment variables:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64  # Adjust path as needed
export SPARK_HOME=/path/to/spark  # If using standalone Spark installation
export PATH=$PATH:$SPARK_HOME/bin
```

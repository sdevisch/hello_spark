# Hello Spark: Start with the conclusion, then dive deep

This repository is an end-to-end learning path for Apache Spark and related Python tooling. Each part has:
- A runnable script that demonstrates the concepts
- A concise markdown overview in `docs/` so you can learn without running code

Main conclusion first:

- In a Spark context, prefer Arrow → pandas and the simplest, widely understood API for most analysis and feature engineering. Use pandas-on-Spark when staying distributed; use Arrow to land in pandas DataFrames when moving off Spark.
- For narrow hot paths that pandas cannot express efficiently, use NumPy or Numba in isolated kernels.
- Then go into details: when and where pandas/NumPy serialize, what to avoid, and Spark-specific tips.

Why pandas (over NumPy/Numba) for the majority of work:
- Productivity and readability: rich DataFrame API, groupby/merge/reshape/time series; far fewer lines for common workloads
- Ecosystem fit: scikit-learn, statsmodels, plotting, IO connectors, datetime/categorical tooling
- Fewer footguns: alignment, missing data semantics, automatic dtype handling; easier review/maintenance for teams
- End-to-end flow: Spark → Arrow → pandas is a first-class, well-supported path; pandas-on-Spark provides API parity when you need to stay distributed
- Operational simplicity: no JIT warm-up, fewer dtype/signature pitfalls, easier debugging and testing

When to deviate to NumPy/Numba:
- Tight numeric kernels on large in-memory arrays where pure vectorization is possible or loops are unavoidable
- Heavy math with simple dtypes that benefit from Numba’s nopython loops (and where you can amortize compile cost)
- You’ve profiled the pipeline, verified a small portion dominates, and a kernel rewrite yields meaningful speedup

This repo is organized to read “last page first”: start from framework choices and Arrow impact, then work backwards to serialization fundamentals, UI, and basics.

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

3. **Run the first Python example (optional)**:
   ```bash
   python 01_basics/01_hello_world_python.py
   ```

## Repository layout (Python) — conclusion first (start here)

- `01_frameworks/` (start here)
  - `01_frameworks_conclusion.py` — Full comparison incl. Arrow analysis and decision guidance
  - `02_frameworks_benchmark.py` — End-to-end framework benchmark
  - `03_framework_xbeta_cashflows.py` — Panel data: xbeta, cashflows, rolling windows
  - Appendix: Numbox
    - `04_numbox_dag_demo.py` — Numbox DAG composition; useful in niche cases
    - `05_numbox_dynamic_dag_demo.py` — Dynamic DAG and reconfiguration demo
- `02_performance/`
  - `01_spark_performance_demo.py` — I/O, UDFs, caching, partitioning, broadcast, persistence
  - `02_spark_data_types_performance.py` — Data types: correctness, right-sizing, joins
  - `03_withcolumn_vs_select.py` — withColumn vs select: chaining cost, Arrow impact, memory
- `03_serialization/`
  - `00_observe_serialization.py` — Use explain() and the UI to spot serialization
  - `01_python_serialization_demo.py` — Arrow vs non-Arrow; UDF impact
  - `02_numpy_serialization_focus.py` — Start in Spark; stay vs convert
  - `03_numpy_serialization_nuances.py` — NumPy C↔Python boundaries
- `04_ui/`
  - `01_spark_ui_demo.py` — Sample jobs and an always-on Spark UI
- `05_basics/`
  - `01_hello_world_python.py` — Basic RDD, DataFrame, and SQL examples

## Recommended run sequence (Python) — last page first

1. Framework comparisons (start here)
   - Read: `docs/01_frameworks.md`
   - Outputs: `docs/generated/01_frameworks_conclusion.md`, `02_frameworks_benchmark.md`, `03_framework_xbeta_cashflows.md`, appendix `04_*` and `05_*`
   ```bash
   python 01_frameworks/01_frameworks_conclusion.py
   python 01_frameworks/02_frameworks_benchmark.py
   python 01_frameworks/03_framework_xbeta_cashflows.py
   # Appendix (optional)
   python 01_frameworks/04_numbox_dag_demo.py
   python 01_frameworks/05_numbox_dynamic_dag_demo.py
   ```
2. Performance patterns
   - Read: `docs/02_performance.md`
   - Outputs: `docs/generated/perf_*_*.md`
   ```bash
   python 02_performance/01_spark_performance_demo.py
   python 02_performance/02_spark_data_types_performance.py
   python 02_performance/03_withcolumn_vs_select.py
   ```
3. Serialization fundamentals
   - Read: `docs/03_serialization.md`
   - Outputs: `docs/generated/ser_*_*.md`
   ```bash
   python 03_serialization/00_observe_serialization.py
   python 03_serialization/01_python_serialization_demo.py
   python 03_serialization/02_numpy_serialization_focus.py
   python 03_serialization/03_numpy_serialization_nuances.py
   ```
4. Spark UI
   - Read: `docs/04_ui.md`
   - Outputs: `docs/generated/ui_01_spark_ui_demo.md`
   ```bash
   python 04_ui/01_spark_ui_demo.py
   ```
5. Basics (optional background)
   - Read: `docs/05_basics.md`

## End-to-End test runner

Use the provided script to run an end-to-end check of the repository examples.

```bash
# Minimal smoke test (recommended first run)
FAST=1 bash scripts/run_e2e.sh

# Full run (will take longer)
bash scripts/run_e2e.sh
```

Notes:
- Requires Java 8 or 11 on PATH for Spark to start.
- Python uses `pyspark==3.3.4` to align with Spark 3.3; install via `requirements.txt`.
- The script also tries to run the Scala example if `sbt` is available.

Notes:
- Some scripts size datasets based on available RAM and may take several minutes.
- Arrow optimizations require `pyarrow` (included in `requirements.txt`).

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

## What the examples demonstrate

Across the path you will see:

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
   - Chaining operations; immutable data transformations

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

## Next steps

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

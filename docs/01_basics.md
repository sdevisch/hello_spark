## Basics (read last)

Scope: essential concepts only. Use DataFrames and built-ins; RDDs for historical context. For decisions, see Frameworks first.

This part introduces core Spark concepts with a single Python script: `01_basics/01_hello_world_python.py`.

### What it covers
- SparkSession and SparkContext
- RDD basics: map, filter, reduce
- DataFrame creation, filtering, aggregations
- Temporary views and simple SQL

### What you would see if you ran it
- Printed lists from RDD transformations (squares, evens)
- DataFrame `.show()` output for people data
- SQL aggregation by city
- Spark version and UI URL

### Key ideas
- Start with a `SparkSession` using `local[*]` for multi-core local execution
- Prefer DataFrames and built-in functions over Python loops
- Use SQL when it improves readability for aggregations

### File
- `01_basics/01_hello_world_python.py`

### Generated output
- `docs/generated/01_basics_output.md`



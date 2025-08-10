## Performance (supporting detail)

Scope: cross-cutting practices that make Frameworks’ conclusion true in practice. Not a replacement for profiling or Serialization mechanics.

This part demonstrates common performance bottlenecks and fixes.

### Files
- `04_performance/08_spark_performance_demo.py`
- `04_performance/09_spark_data_types_performance.py`

### Generated outputs
- `docs/generated/perf_01_spark_performance_demo.md`
- `docs/generated/perf_02_spark_data_types_performance.md`

### What they cover
- I/O formats: CSV vs Parquet (read/write speed)
- Serialization issues: Python UDF vs native functions
- Caching and persistence strategies
- Partitioning strategies and broadcast joins
- Data type choices: strings vs typed, 64-bit vs right-sized

### Key takeaways
- Use Parquet over CSV for faster I/O
- Cache reused DataFrames; choose appropriate storage levels
- Use 2–3 partitions per CPU core for local workloads
- Broadcast small tables to avoid shuffles
- Right-size types; avoid string-typed columns



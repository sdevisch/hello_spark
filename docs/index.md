## Hello Spark: Docs Index (conclusion first)

How to read this (Pyramid Principle):
- Start with the conclusion (framework choice), then supporting reasons (performance), then deeper mechanics (serialization), then tooling (UI), then basics.
- Each section is scoped to avoid overlap (mutually exclusive) and together they cover the full story (collectively exhaustive).

Reading order and scope

1) Frameworks — What to use and why (start here)
  - Overview doc: 01_frameworks.md
- Scope: conclusions and decision framework; when to stay in Spark, when to use Arrow→pandas, and when to isolate NumPy/Numba kernels.
- Not covered: low-level serialization details or generic perf tips (see below).
  - [01_frameworks_conclusion.md](generated/01_frameworks_conclusion.md)
  - [02_frameworks_benchmark.md](generated/02_frameworks_benchmark.md)
  - [03_framework_xbeta_cashflows.md](generated/03_framework_xbeta_cashflows.md)
  - Appendix (niche DAG structuring):
    - [04_numbox_dag_demo.md](generated/04_numbox_dag_demo.md)
    - [05_numbox_dynamic_dag_demo.md](generated/05_numbox_dynamic_dag_demo.md)

2) Performance — Cross-cutting patterns that support the conclusion
  - Overview doc: 02_performance.md
- Scope: IO formats, UDF vs native, caching, partitioning, broadcast, persistence, types.
- Not covered: Spark↔Python boundary mechanics (see Serialization).
  - [perf_01_spark_performance_demo.md](generated/perf_01_spark_performance_demo.md)
  - [perf_02_spark_data_types_performance.md](generated/perf_02_spark_data_types_performance.md)

3) Serialization — Mechanics of Spark↔pandas/NumPy boundaries
  - Overview doc: 03_serialization.md
- Scope: explain plans, where Python shows up, Arrow vs non-Arrow, NumPy C↔Python boundaries, best practices.
- Not covered: framework selection or cluster-level tuning.
  - [ser_00_observe_serialization.md](generated/ser_00_observe_serialization.md)
  - [ser_01_python_serialization_demo.md](generated/ser_01_python_serialization_demo.md)
  - [ser_02_numpy_serialization_focus.md](generated/ser_02_numpy_serialization_focus.md)
  - [ser_03_numpy_serialization_nuances.md](generated/ser_03_numpy_serialization_nuances.md)

4) UI — Observe execution to connect code to runtime
  - Overview doc: 04_ui.md
5) Basics — Background concepts
  - Overview doc: 05_basics.md
- Scope: quick jobs to populate the UI and learn to interpret stages/plans.
  - [ui_01_spark_ui_demo.md](generated/ui_01_spark_ui_demo.md)

Notes
- Prefer Spark native; when moving off Spark use Arrow→pandas; only isolate NumPy/Numba for profiled hotspots.
- Cross-links at the top of scripts point back here.



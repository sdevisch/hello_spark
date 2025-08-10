## Frameworks: Start with the conclusion

Main guidance:

- In a Spark context, prefer Arrow and pandas for the majority of tasks. Use Spark native functions when you stay in Spark; when converting to single-machine, use Arrow to pandas and keep operations vectorized in pandas.
- For specialized kernels or tight loops that pandas cannot express efficiently, switch to NumPy or Numba (jitted NumPy) as isolated steps. The scripts here show those niche cases.

Then, the details: conversion times, compute-only comparisons, and serialization hotspots.

### Files (conclusion → supporting → appendix)
- `05_frameworks/01_frameworks_conclusion.py`
- `05_frameworks/02_frameworks_benchmark.py`
- `05_frameworks/03_framework_xbeta_cashflows.py`
- `05_frameworks/04_numbox_dag_demo.py` (appendix)
- `05_frameworks/05_numbox_dynamic_dag_demo.py` (appendix)

### Generated outputs
- `docs/generated/01_frameworks_conclusion.md`
- `docs/generated/02_frameworks_benchmark.md`
- `docs/generated/03_framework_xbeta_cashflows.md`
- `docs/generated/04_numbox_dag_demo.md`
- `docs/generated/05_numbox_dynamic_dag_demo.md`

### What they cover
- Overall conclusion and decision framework (01)
- Supporting benchmarks and breakdowns (02)
- Case study: panel xbeta and cashflows (03)
- Appendix: Numbox DAG demos (04–05)

### Typical performance hierarchy (may vary by workload)
- Jitted NumPy (Numba) and NumPy are fastest for pure numerical array kernels when data fits in memory
- Pandas is generally fast and productive for mixed data types and tabular ops on a single machine
- Spark is the right choice when you need scale-out, fault tolerance, or big data integrations
  
Appendix: When modularizing pipelines into a DAG, Numbox can provide structure and JIT reuse in niche scenarios. See `https://github.com/Goykhman/numbox`.

### Key takeaways
- Choose the right tool for the job based on data size and workload
- Consider total cost: compute + conversion
- Arrow accelerates Spark↔pandas
- JIT compilation helps when vectorization isn’t possible



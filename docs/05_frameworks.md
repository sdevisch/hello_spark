## Frameworks: Spark, Pandas, NumPy, and Numba

This part compares frameworks on realistic workloads and synthetic benchmarks.

### Files
- `05_frameworks/10_framework_xbeta_cashflows.py`
- `05_frameworks/11_comprehensive_performance_benchmark.py`
- `05_frameworks/12_comprehensive_framework_comparison.py`
- `05_frameworks/13_numbox_dag_demo.py`
- `05_frameworks/14_numbox_dynamic_dag_demo.py`

### Generated outputs
- `docs/generated/05_frameworks_xbeta_cashflows_output.md`
- `docs/generated/05_frameworks_benchmark_output.md`
- `docs/generated/05_frameworks_comparison_output.md`
- `docs/generated/13_numbox_dag_demo.md`
- `docs/generated/14_numbox_dynamic_dag_demo.md`

### What they cover
- Panel dataset with per-entity features, xbeta, cashflows, and rolling windows
- End-to-end benchmarks across Spark, pandas, NumPy, and Numba
- Arrow impact on conversion speed and total pipeline time
- Numbox DAG demo: building a DAG of typed JIT kernels using Numbox `Node`, `Work`, and `Proxy` to structure complex pipelines and compare against NumPy/Numba
- Numbox Dynamic DAG demo: runtime reconfiguration of feature graph (varying transforms and degrees per micro-batch), showcasing Proxy caching and Node type-erased dependencies

### Typical performance hierarchy (may vary)
1. Jitted NumPy (Numba)
2. NumPy (vectorized)
3. Pandas (vectorized)
4. Spark (distributed; scales far beyond memory)
  
Additionally, when modularizing pipelines into a DAG, Numbox can provide structure and JIT reuse. See `https://github.com/Goykhman/numbox`.

### Key takeaways
- Choose the right tool for the job based on data size and workload
- Consider total cost: compute + conversion
- Arrow accelerates Spark↔pandas
- JIT compilation helps when vectorization isn’t possible



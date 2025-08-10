## Frameworks: Spark, Pandas, NumPy, and Numba

This part compares frameworks on realistic workloads and synthetic benchmarks.

### Files
- `05_frameworks/10_framework_xbeta_cashflows.py`
- `05_frameworks/11_comprehensive_performance_benchmark.py`
- `05_frameworks/12_comprehensive_framework_comparison.py`

### Generated outputs
- `docs/generated/05_frameworks_xbeta_cashflows_output.md`
- `docs/generated/05_frameworks_benchmark_output.md`
- `docs/generated/05_frameworks_comparison_output.md`

### What they cover
- Panel dataset with per-entity features, xbeta, cashflows, and rolling windows
- End-to-end benchmarks across Spark, pandas, NumPy, and Numba
- Arrow impact on conversion speed and total pipeline time

### Typical performance hierarchy (may vary)
1. Jitted NumPy (Numba)
2. NumPy (vectorized)
3. Pandas (vectorized)
4. Spark (distributed; scales far beyond memory)

### Key takeaways
- Choose the right tool for the job based on data size and workload
- Consider total cost: compute + conversion
- Arrow accelerates Spark↔pandas
- JIT compilation helps when vectorization isn’t possible



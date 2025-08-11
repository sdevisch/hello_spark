## Frameworks: Start with the conclusion (read first)

Main guidance (refined with the new package-vs-Spark experiment):

- Use Spark native functions when staying distributed. If converting to a single machine, use Arrow → pandas for general tabular work.
- For compute-heavy numeric kernels with iterative loops (e.g., multi-period forecasts), a dedicated NumPy/Numba package can outperform pandas-on-Spark and pure Spark—provided the dataset or working set fits in memory or can be partitioned safely. In such cases: Spark for ETL, Arrow → pandas (or distributed mapPartitions), then run compiled kernels.
- Prefer pandas for mixed-type tabular transformations, joins, reshaping, feature engineering, and when developer productivity and readability dominate.

Why pandas first (for most tabular work):
- Expressiveness: concise groupby/join/reshape/time series vs hand-rolled array logic
- Interop: seamless with scikit-learn, plotting, IO; fewer bespoke adapters
- Team velocity: clearer code reviews, fewer dtype pitfalls, easier onboarding
- Proven handoff: Spark → Arrow → pandas is optimized and stable; pandas-on-Spark offers API parity when staying distributed

When NumPy/Numba shine (new evidence):
- Dense numeric kernels with significant arithmetic intensity and iterative recurrences (our `06_package_vs_pandas_on_spark.py` experiment).
- You’ve profiled and identified hotspots that map cleanly to arrays. Kernels can be isolated in a package and reused.
- Data fits in driver memory (Arrow path) or can be processed per-partition with mapPartitions.

Structure:
- Conclusion and decision criteria (this page)
- Supporting benchmarks (Performance)
- Mechanics (Serialization)
- Tooling (UI)

### Files (conclusion → supporting → appendix)
- `01_frameworks/01_frameworks_conclusion.py`
- `01_frameworks/02_frameworks_benchmark.py`
- `01_frameworks/03_framework_xbeta_cashflows.py`
- `01_frameworks/04_numbox_dag_demo.py` (appendix)
- `01_frameworks/05_numbox_dynamic_dag_demo.py` (appendix)

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

### Typical performance hierarchy (depends on workload)
- Jitted NumPy (Numba) / NumPy: fastest for pure numeric array kernels when data fits in memory or when run per-partition.
- Pandas: generally fast and highly productive for mixed-type tabular ops on a single machine.
- Spark: best for scale-out, joins/shuffles on large data, and avoiding Python serialization; use native expressions where possible.

New comparison added: `06_package_vs_pandas_on_spark.py` and `docs/generated/06_package_vs_pandas_on_spark.md` show:
- Package (NumPy/Numba) after Arrow beats pandas-on-Spark and pure Spark when horizon (iterations) is large and compute dominates.
- Distributed NumPy without Arrow (mapPartitions) is viable but pays Python serialization costs; still useful if kernels are heavy enough and memory is constrained.
  
Appendix: When modularizing pipelines into a DAG, Numbox can provide structure and JIT reuse in niche scenarios. See `https://github.com/Goykhman/numbox`.

### Key takeaways
- Choose the right tool for the job based on data size and workload
- Consider total cost: compute + conversion
- Arrow accelerates Spark↔pandas
- JIT compilation helps when vectorization isn’t possible



# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 01:16 UTC

## Console output

```text
🚀 Package vs pandas-on-Spark experiment
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB

================================================================================
🧪 Scenario: Small, in-memory compute-heavy (Numba sweet spot)
--------------------------------------------------------------------------------
rows=300,000, entities=500, horizon=48, wide_cols=0
~Estimated raw size (double-eqv): 0.01 GB
   Built panel rows: 300,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.450s; transform: 0.179s; forecast: 0.189s

== pandas-on-Spark path: keep work in Spark plan ==
/Users/sdevisch/repos/hello_spark/.venv311/lib/python3.11/site-packages/pyspark/pandas/__init__.py:50: UserWarning: 'PYARROW_IGNORE_TIMEZONE' environment variable was not set. It is required to set this environment variable to '1' in both driver and executor sides if you use pyarrow>=2.0.0. pandas-on-Spark will set it for you but it does not work if there is a Spark context already launched.
  warnings.warn(
   pandas-on-Spark unavailable: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

📊 Scenario summary:
   Package path total: 0.817s  (convert=0.450s, tf=0.179s, fc=0.189s, numba=True)
   pandas-on-Spark total: n/a (ps unavailable)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Medium, some width (balanced)
--------------------------------------------------------------------------------
rows=600,000, entities=1,000, horizon=36, wide_cols=50
~Estimated raw size (double-eqv): 0.27 GB
   Built panel rows: 600,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.244s; transform: 0.001s; forecast: 0.050s

== pandas-on-Spark path: keep work in Spark plan ==
   pandas-on-Spark unavailable: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

📊 Scenario summary:
   Package path total: 0.295s  (convert=0.244s, tf=0.001s, fc=0.050s, numba=True)
   pandas-on-Spark total: n/a (ps unavailable)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Wide (hundreds cols), moderate horizon
--------------------------------------------------------------------------------
rows=400,000, entities=1,000, horizon=24, wide_cols=200
~Estimated raw size (double-eqv): 0.66 GB
   Built panel rows: 400,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.475s; transform: 0.001s; forecast: 0.022s

== pandas-on-Spark path: keep work in Spark plan ==
   pandas-on-Spark unavailable: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

📊 Scenario summary:
   Package path total: 0.498s  (convert=0.475s, tf=0.001s, fc=0.022s, numba=True)
   pandas-on-Spark total: n/a (ps unavailable)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.

================================================================================
🧪 Scenario: Large rows (driver-safety block), horizon small
--------------------------------------------------------------------------------
rows=2,000,000, entities=2,000, horizon=12, wide_cols=50
~Estimated raw size (double-eqv): 0.90 GB
   Built panel rows: 2,000,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.444s; transform: 0.006s; forecast: 0.046s

== pandas-on-Spark path: keep work in Spark plan ==
   pandas-on-Spark unavailable: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

📊 Scenario summary:
   Package path total: 0.495s  (convert=0.444s, tf=0.006s, fc=0.046s, numba=True)
   pandas-on-Spark total: n/a (ps unavailable)

🧭 Guidance:
   • Package path excels when compute is heavy (large horizon) and data fits in memory.
   • pandas-on-Spark wins when width/rows are large and loops are short or vectorizable.
```

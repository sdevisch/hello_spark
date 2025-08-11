# Frameworks: Package (Numba/NumPy) vs pandas-on-Spark

Generated: 2025-08-11 01:10 UTC

## Console output

```text
🚀 Package vs pandas-on-Spark experiment
📚 Docs index: docs/index.md
💻 System memory: 18.0 GB
   Built panel rows: 1,000,000

== Package path: Spark → pandas (Arrow) → NumPy/Numba kernels ==
   Convert (Arrow): 0.960s; transform: 0.278s; forecast: 0.254s

== pandas-on-Spark path: keep work in Spark plan ==
/Users/sdevisch/repos/hello_spark/.venv311/lib/python3.11/site-packages/pyspark/pandas/__init__.py:50: UserWarning: 'PYARROW_IGNORE_TIMEZONE' environment variable was not set. It is required to set this environment variable to '1' in both driver and executor sides if you use pyarrow>=2.0.0. pandas-on-Spark will set it for you but it does not work if there is a Spark context already launched.
  warnings.warn(
   pandas-on-Spark unavailable: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

🏁 Summary (lower is better):
   Package path total: 1.491s  (convert=0.960s, tf=0.278s, fc=0.254s, numba=True)

📌 When package+Numba is better:
   • Compute-heavy transforms and iterative loops per entity
   • Horizon is large (dozens), tight recurrence relations
   • Data fits on driver; conversion cost amortized

📌 When pandas-on-Spark is better:
   • Data larger-than-memory; need distributed execution
   • Group/window operations without tight per-row recurrences
   • You want to avoid driver collection and package distribution
```

## Serialization (mechanics)

Scope: how and where serialization happens; how to avoid unnecessary boundaries. Decisions live in Frameworks; performance heuristics in Performance.

This part contains four scripts that show where serialization happens and how to minimize it.

### Files
- `03_serialization/04_observe_serialization.py`
- `03_serialization/05_python_serialization_demo.py`
- `03_serialization/06_numpy_serialization_focus_clean.py`
- `03_serialization/07_numpy_serialization_nuances.py`

### Generated outputs
- `docs/generated/ser_00_observe_serialization.md`
- `docs/generated/ser_01_python_serialization_demo.md`
- `docs/generated/ser_02_numpy_serialization_focus.md`
- `docs/generated/ser_03_numpy_serialization_nuances.md`

### What they cover
- Using `explain()` to spot `BatchEvalPython` (serialization for Python UDFs)
- Spark→pandas conversions with and without Arrow
- When to stay in Spark vs convert to NumPy/pandas
- NumPy operations that stay in C vs those that cross into Python

### Key takeaways (recap)
- Prefer native Spark functions over Python UDFs
- Enable Arrow for faster Spark↔pandas conversions; use Arrow when moving to pandas
- Stay within one framework as long as possible
- Avoid `.tolist()` and frequent scalar extraction in tight loops



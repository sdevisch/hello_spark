## Serialization: Explain plans, Arrow, and NumPy boundaries

Read this after the framework conclusions. The goal here is to explain when pandas/NumPy serialize, why Arrow matters, and how to avoid hidden Python crossings.

This part contains four scripts that show where serialization happens and how to minimize it.

### Files
- `03_serialization/04_observe_serialization.py`
- `03_serialization/05_python_serialization_demo.py`
- `03_serialization/06_numpy_serialization_focus_clean.py`
- `03_serialization/07_numpy_serialization_nuances.py`

### Generated outputs
- `docs/generated/03_serialization_observe_output.md`
- `docs/generated/03_serialization_python_demo_output.md`
- `docs/generated/03_serialization_numpy_focus_output.md`
- `docs/generated/03_serialization_numpy_nuances_output.md`

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



import importlib.util
import pathlib
import pytest

from pyspark.sql import SparkSession, functions as F


def _load_benchmark():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "02_performance" / "03_withcolumn_vs_select.py"
    spec = importlib.util.spec_from_file_location("withcol_vs_select", str(module_path))
    mod = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod.WithColumnVsSelectBenchmark


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder.appName("withcolumn-vs-select-tests")
        .master("local[*]")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    yield spark
    spark.stop()


def test_withcolumn_and_select_produce_same_result(spark):
    Bench = _load_benchmark()
    bench = Bench()
    bench.spark = spark

    rows = 50_000
    base = bench._generate_df(rows)

    df_with = bench._withcolumn_chain(base)
    df_sel = bench._select_combined(base)

    last_col = "j"

    # Both pipelines must yield the same sum on the last derived column
    sum_with = df_with.agg(F.sum(F.col(last_col)).alias("s")).collect()[0]["s"]
    sum_sel = df_sel.agg(F.sum(F.col(last_col)).alias("s")).collect()[0]["s"]

    assert sum_with == sum_sel
    assert sum_with is not None


def test_sum_scales_with_rows(spark):
    Bench = _load_benchmark()
    bench = Bench()
    bench.spark = spark

    base_small = bench._generate_df(10_000)
    base_large = bench._generate_df(100_000)

    last_col = "j"

    small_sum = bench._select_combined(base_small).agg(F.sum(F.col(last_col)).alias("s")).collect()[0]["s"]
    large_sum = bench._select_combined(base_large).agg(F.sum(F.col(last_col)).alias("s")).collect()[0]["s"]

    # With larger row counts, aggregated sum should increase
    assert large_sum > small_sum


def test_last_column_exists_and_is_used(spark):
    Bench = _load_benchmark()
    bench = Bench()
    bench.spark = spark

    base = bench._generate_df(1_000)
    df = bench._withcolumn_chain(base)
    last_col = "j"

    # Schema contains the last derived column
    assert last_col in df.columns

    # Aggregation references last column and returns a non-null result
    result = df.agg(F.sum(F.col(last_col)).alias("s")).collect()[0]["s"]
    assert result is not None



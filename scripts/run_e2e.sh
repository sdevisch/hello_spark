#!/usr/bin/env bash
set -euo pipefail

echo "==> Hello Spark: End-to-End test runner"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAST_MODE="${FAST:-0}"

echo "==> Using repo root: $REPO_ROOT"

echo "==> Environment checks"
if command -v java >/dev/null 2>&1; then
  echo "Java version:" && java -version || true
else
  echo "WARNING: Java not found on PATH. Spark may fail to start."
fi

if command -v python3 >/dev/null 2>&1; then
  echo "Python version:" && python3 -V
else
  echo "ERROR: python3 not found on PATH" >&2
  exit 1
fi

echo "==> Installing Python dependencies (requirements.txt)"
python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install -r requirements.txt

# Help Spark bind locally in some environments
export SPARK_LOCAL_IP=${SPARK_LOCAL_IP:-127.0.0.1}

run_py() {
  local script_path="$1"
  echo "\n==> Running: $script_path"
  python3 "$script_path"
}

if [[ "$FAST_MODE" == "1" ]]; then
  echo "==> FAST=1 enabled: Running a minimal smoke set"
  run_py 05_basics/01_hello_world_python.py
  run_py 02_performance/01_spark_performance_demo.py
else
  echo "==> Running full Python suite"
  # 01_frameworks
  run_py 01_frameworks/01_frameworks_conclusion.py
  run_py 01_frameworks/02_frameworks_benchmark.py
  run_py 01_frameworks/03_framework_xbeta_cashflows.py
  run_py 01_frameworks/04_numbox_dag_demo.py
  run_py 01_frameworks/05_numbox_dynamic_dag_demo.py

  # 02_performance
  run_py 02_performance/01_spark_performance_demo.py
  run_py 02_performance/02_spark_data_types_performance.py

  # 03_serialization
  run_py 03_serialization/00_observe_serialization.py
  run_py 03_serialization/01_python_serialization_demo.py
  run_py 03_serialization/02_numpy_serialization_focus.py
  run_py 03_serialization/03_numpy_serialization_nuances.py

  # 04_ui
  run_py 04_ui/01_spark_ui_demo.py

  # 05_basics
  run_py 05_basics/01_hello_world_python.py
fi

echo "\n==> Python suite completed successfully"

if [[ "${RUN_SCALA:-0}" == "1" ]]; then
  if command -v sbt >/dev/null 2>&1; then
    echo "\n==> Running Scala example via SBT"
    sbt -v "runMain HelloWorldSpark" | cat || echo "Scala example failed; continuing Python E2E"
  else
    echo "\n==> SBT not found; skipping Scala example"
  fi
else
  echo "\n==> RUN_SCALA not set; skipping Scala example (set RUN_SCALA=1 to enable)"
fi

echo "\n==> E2E test runner finished successfully"



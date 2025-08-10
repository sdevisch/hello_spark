import io
import os
import sys
from datetime import datetime


def _infer_scope(markdown_path: str) -> str | None:
    base = os.path.basename(markdown_path)
    # Frameworks
    if base.startswith("01_frameworks_conclusion"):
        return (
            "Conclusion and decision framework: when to stay in Spark, when to use "
            "Arrow→pandas, and when to isolate NumPy/Numba kernels."
        )
    if base.startswith("02_frameworks_benchmark"):
        return "Supporting benchmark for the frameworks conclusion."
    if base.startswith("03_framework_xbeta_cashflows"):
        return "Case study supporting the frameworks conclusion (panel xbeta & cashflows)."
    if base.startswith("04_numbox_dag_demo") or base.startswith("05_numbox_dynamic_dag_demo"):
        return "Appendix: niche DAG structuring (Numbox) for specialized scenarios."
    # Performance
    if base.startswith("perf_"):
        return (
            "Cross-cutting performance practices: IO formats, UDF vs native, caching, "
            "partitioning, broadcast, and data types."
        )
    # Serialization
    if base.startswith("ser_00_observe_serialization"):
        return "Observe where Python shows up (explain/UI) and how to spot serialization."
    if base.startswith("ser_01_"):
        return "Spark→pandas with/without Arrow; Python UDF overhead; practical guidance."
    if base.startswith("ser_02_"):
        return "Spark→NumPy focus: total cost and when conversion pays off."
    if base.startswith("ser_03_"):
        return "NumPy C↔Python boundaries and best practices to avoid Python crossings."
    # UI
    if base.startswith("ui_"):
        return "Tooling: use the Spark UI to connect code to execution (jobs/stages/SQL)."
    return None


def run_and_save_markdown(markdown_path: str, title: str, main_callable) -> None:
    os.makedirs(os.path.dirname(markdown_path), exist_ok=True)

    # Capture stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    buffer = io.StringIO()
    sys.stdout = buffer
    sys.stderr = buffer
    error: Exception | None = None

    try:
        # Ensure project root is importable for utils.* imports in scripts
        repo_root = os.path.abspath(os.path.join(os.path.dirname(markdown_path), "..", ".."))
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        main_callable()
    except SystemExit:
        # Allow scripts that call sys.exit to still generate docs
        pass
    except Exception as e:  # noqa: BLE001
        error = e
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    output = buffer.getvalue()

    # Compose markdown
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    scope = _infer_scope(markdown_path)

    lines = [
        f"# {title}",
        "",
        f"Generated: {ts}",
        "",
    ]
    if scope:
        lines += [
            "## Scope",
            "",
            scope,
            "",
        ]
    lines += [
        "## Console output",
        "",
        "```text",
        output.strip(),
        "```",
    ]
    if error is not None:
        lines += [
            "",
            "## Generation status",
            "",
            f"Encountered error during run: {error}",
        ]

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")



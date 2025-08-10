import io
import os
import sys
from datetime import datetime


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
    lines = [
        f"# {title}",
        "",
        f"Generated: {ts}",
        "",
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



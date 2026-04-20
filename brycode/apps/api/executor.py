"""Execute user-submitted Python code in a subprocess with a timeout."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
import tempfile
import os


def execute_solution(
    code: str,
    method_name: str,
    args: dict,
    timeout: int = 5,
) -> tuple[object | None, str | None, str | None]:
    """
    Run user code in an isolated subprocess.

    Returns (result, error, stdout):
      - On success: (parsed_return_value, None, captured_stdout)
      - On failure: (None, error_message, captured_stdout)
    """

    args_json = json.dumps(args)

    # The wrapper captures all user print() output separately from the result.
    # It redirects stdout to a StringIO during execution, then outputs a JSON
    # envelope with both the return value and any captured prints.
    wrapper = textwrap.dedent(f"""\
        import json, sys, io

        # ── User code ──
        {_indent(code, 8).strip()}
        # ── End user code ──

        _args = json.loads('''{args_json}''')

        # Redirect stdout to capture print statements
        _old_stdout = sys.stdout
        _captured = io.StringIO()
        sys.stdout = _captured

        try:
            _sol = Solution()
            _result = _sol.{method_name}(**_args)
        finally:
            sys.stdout = _old_stdout

        _stdout_text = _captured.getvalue()

        # Output as JSON envelope to real stdout
        print(json.dumps({{"result": _result, "stdout": _stdout_text}}))
    """)

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as tmp:
            tmp.write(wrapper)
            tmp_path = tmp.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            error = result.stderr.strip()
            error = error.replace(tmp_path, "<solution>")
            return None, error, None

        stdout = result.stdout.strip()
        if not stdout:
            return None, "No output produced. Make sure your function returns a value.", None

        try:
            envelope = json.loads(stdout)
            return (
                envelope.get("result"),
                None,
                envelope.get("stdout") or None,
            )
        except json.JSONDecodeError:
            return None, f"Could not parse output: {stdout}", None

    except subprocess.TimeoutExpired:
        return None, f"Time Limit Exceeded ({timeout}s)", None
    except Exception as e:
        return None, f"Execution error: {{str(e)}}", None
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _indent(text: str, spaces: int) -> str:
    """Indent every line of text by the given number of spaces."""
    prefix = " " * spaces
    return "\n".join(prefix + line for line in text.splitlines())

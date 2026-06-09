import os
import sys
import io
import time
import tracemalloc
import traceback
import inspect
import resource
from typing import List
from collections import deque

from app.dsa import (
    ListNode,
    TreeNode,
    TrieNode,
    preprocess_input,
    EVAL_GLOBALS,
    args_from,
    parse_val,
    normalize_val,
    fmt_val,
)


def get_vms_bytes():
    try:
        with open("/proc/self/statm", "r") as f:
            vms_pages = int(f.read().split()[0])
            return vms_pages * os.sysconf("SC_PAGE_SIZE")
    except Exception:
        return 128 * 1024 * 1024


def execute_case(
    user_code, fn_name, is_class, input_str, expected_str, time_limit_ms, mem_limit_mb
):
    buf = io.StringIO()
    sys.stdout = buf

    ns = {
        "ListNode": ListNode,
        "TreeNode": TreeNode,
        "TrieNode": TrieNode,
        "List": List,
        "deque": deque,
        "math": __import__("math"),
        "collections": __import__("collections"),
        "heapq": __import__("heapq"),
        "bisect": __import__("bisect"),
        "itertools": __import__("itertools"),
        "functools": __import__("functools"),
        "re": __import__("re"),
        "string": __import__("string"),
    }

    err = None
    mem_err = False
    result = None
    elapsed_ms = 0.0
    peak_mb = 0.0
    old_limit = None
    t0 = None

    if mem_limit_mb:
        try:
            current_vms = get_vms_bytes()
            limit_bytes = current_vms + (mem_limit_mb * 1024 * 1024)
            soft_h, hard_h = resource.getrlimit(resource.RLIMIT_AS)
            limit_bytes = (
                min(limit_bytes, hard_h)
                if hard_h != resource.RLIM_INFINITY
                else limit_bytes
            )
            resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, hard_h))
            old_limit = (soft_h, hard_h)
        except Exception:
            pass

    try:
        exec(user_code, ns)

        if is_class:
            pp = preprocess_input(input_str)
            eval_globals = dict(EVAL_GLOBALS)
            eval_globals.update(
                {
                    "ListNode": ListNode,
                    "TreeNode": TreeNode,
                    "TrieNode": TrieNode,
                }
            )
            ops = eval("[" + pp + "]", eval_globals)
            if len(ops) == 1 and isinstance(ops[0], list) and ops[0] and isinstance(ops[0][0], list):
                ops = ops[0]
            cls = ns.get(ops[0][0])
            if cls is None:
                raise RuntimeError(f"Class '{ops[0][0]}' is not defined.")

            tracemalloc.start()
            t0 = time.perf_counter()

            constructor_args = ops[0][1] if len(ops[0]) > 1 and isinstance(ops[0][1], list) else ops[0][1:]
            obj = cls(*constructor_args)
            out = [None]
            for op in ops[1:]:
                method_args = op[1] if len(op) > 1 and isinstance(op[1], list) else op[1:]
                out.append(getattr(obj, op[0])(*method_args))
            result = out

            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_mb = peak / (1024 * 1024)
        else:
            fn = ns.get(fn_name)
            if fn is None:
                raise RuntimeError(f"Function '{fn_name}' is not defined.")

            args = args_from(input_str)

            sig = inspect.signature(fn)
            params = list(sig.parameters.keys())

            tracemalloc.start()
            t0 = time.perf_counter()

            if params and params[0] == "self":

                class DummySelf:
                    pass

                result = fn(DummySelf(), *args)
            else:
                result = fn(*args)

            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_mb = peak / (1024 * 1024)

    except MemoryError:
        mem_err = True
        if t0 is not None:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
        try:
            _, peak = tracemalloc.get_traced_memory()
            peak_mb = peak / (1024 * 1024)
            tracemalloc.stop()
        except Exception:
            pass
        if mem_limit_mb:
            peak_mb = max(peak_mb, float(mem_limit_mb))
    except Exception:
        err = traceback.format_exc()
        if t0 is not None:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
        try:
            _, peak = tracemalloc.get_traced_memory()
            peak_mb = peak / (1024 * 1024)
            tracemalloc.stop()
        except Exception:
            pass
    finally:
        if old_limit:
            try:
                resource.setrlimit(resource.RLIMIT_AS, old_limit)
            except Exception:
                pass

    sys.stdout = sys.__stdout__

    stdout_val = buf.getvalue()
    if len(stdout_val) > 50000:
        stdout_val = stdout_val[:50000] + "\n... [Stdout Truncated]"

    err_val = err
    if err_val and len(err_val) > 50000:
        err_val = err_val[:50000] + "\n... [Error Truncated]"

    base = {
        "stdout": stdout_val,
        "timeMs": elapsed_ms,
        "memMb": peak_mb,
    }

    if mem_err:
        base.update({"status": "MLE", "error": "Memory Limit Exceeded", "output": None})
    elif err_val is not None:
        base.update({"status": "RE", "error": err_val, "output": None})
    elif time_limit_ms and elapsed_ms > time_limit_ms:
        base.update({"status": "TLE", "error": "Time Limit Exceeded", "output": None})
    elif mem_limit_mb and peak_mb > mem_limit_mb:
        base.update({"status": "MLE", "error": "Memory Limit Exceeded", "output": None})
    else:
        expected = parse_val(expected_str)
        nr = normalize_val(result)
        ne = normalize_val(expected)
        try:
            ok = nr == ne
        except Exception:
            ok = False

        raw_output = fmt_val(result)
        if len(raw_output) > 50000:
            raw_output = raw_output[:50000] + "... [Output Truncated]"

        base.update(
            {"status": "AC" if ok else "WA", "error": None, "output": raw_output}
        )

    return base

const PYODIDE_VERSION = "0.27.7";
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

const PREAMBLE = `
from typing import List, Dict, Set, Tuple, Optional, Union, Any, Callable, Deque
import collections, heapq, math, bisect, itertools, functools, re, string
from collections import defaultdict, deque, Counter, OrderedDict
from heapq import heappush, heappop, heapify, heappushpop, heapreplace, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from math import sqrt, ceil, floor, gcd, inf, nan
from functools import lru_cache, cache, reduce
`;

const FRAMEWORK = `
import sys, io, json, traceback, time, tracemalloc, re as __re

__USER = {}

class __Self:
    pass

def __fmt(v):
    if v is True:
        return "True"
    if v is False:
        return "False"
    if v is None:
        return "None"
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(__fmt(x) for x in v) + "]"
    if isinstance(v, tuple):
        return "(" + ", ".join(__fmt(x) for x in v) + ")"
    if isinstance(v, dict):
        return "{" + ", ".join(json.dumps(k) + ": " + __fmt(val) for k, val in v.items()) + "}"
    try:
        return json.dumps(v)
    except Exception:
        return repr(v)

def __parse(s):
    g = {"true": True, "false": False, "null": None}
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return eval(s, dict(g))
    except Exception:
        return s

def __split_top(s):
    parts = []
    depth = 0
    quote = None
    cur = ""
    prev = ""
    for ch in s:
        if quote:
            cur += ch
            if ch == quote and prev != "\\\\":
                quote = None
        elif ch in "\\"'":
            quote = ch
            cur += ch
        elif ch in "([{":
            depth += 1
            cur += ch
        elif ch in ")]}":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
        prev = ch
    if cur.strip():
        parts.append(cur)
    return parts

__assign_re = __re.compile(r"^\\s*[A-Za-z_]\\w*\\s*=(?!=)")

def __args_from(input_str):
    g = {"true": True, "false": False, "null": None}
    parts = __split_top(input_str)
    if parts and all(__assign_re.match(p) for p in parts):
        ns = {}
        try:
            for p in parts:
                exec(p.strip(), g, ns)
            if ns:
                return list(ns.values())
        except Exception:
            pass
    if parts:
        return [__parse(p.strip()) for p in parts]
    return [__parse(input_str)]

def __prime(src):
    global __USER
    ns = {}
    try:
        exec(${JSON.stringify(PREAMBLE)}, ns)
        exec(src, ns)
        __USER = ns
        return None
    except Exception:
        __USER = {}
        return traceback.format_exc()

def __run_call(fn_name, is_class, input_str):
    if is_class:
        ops = eval("[" + input_str + "]", {"true": True, "false": False, "null": None})
        cls = __USER.get(ops[0][0])
        if cls is None:
            raise RuntimeError("Class '%s' is not defined." % ops[0][0])
        obj = cls(*ops[0][1:])
        out = [None]
        for op in ops[1:]:
            out.append(getattr(obj, op[0])(*op[1:]))
        return out
    fn = __USER.get(fn_name)
    if fn is None:
        raise RuntimeError("Function '%s' is not defined." % fn_name)
    return fn(__Self(), *__args_from(input_str))

def __grade_one(fn_name, is_class, input_str, expected_str, time_limit_ms, mem_limit_mb):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    tracemalloc.start()
    t0 = time.perf_counter()
    err = None
    mem_err = False
    result = None
    try:
        result = __run_call(fn_name, is_class, input_str)
    except MemoryError:
        mem_err = True
    except Exception:
        err = traceback.format_exc()
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    sys.stdout = old
    peak_mb = peak / (1024 * 1024)
    base = {"stdout": buf.getvalue(), "timeMs": elapsed_ms, "memMb": peak_mb}
    if mem_err:
        base.update({"status": "MLE", "error": "Memory Limit Exceeded", "output": None})
    elif err is not None:
        base.update({"status": "RE", "error": err, "output": None})
    elif time_limit_ms and elapsed_ms > time_limit_ms:
        base.update({"status": "TLE", "error": "Time Limit Exceeded", "output": None})
    elif mem_limit_mb and peak_mb > mem_limit_mb:
        base.update({"status": "MLE", "error": "Memory Limit Exceeded", "output": None})
    else:
        expected = __parse(expected_str)
        try:
            ok = result == expected
        except Exception:
            ok = False
        base.update({"status": "AC" if ok else "WA", "error": None, "output": __fmt(result)})
    return json.dumps(base)
`;

let py = null;

self.onmessage = async (e) => {
    const msg = e.data;

    if (msg.type === "init") {
        if (py) {
            self.postMessage({ type: "ready" });
            return;
        }
        try {
            const { loadPyodide } = await import(
                /* @vite-ignore */ `${PYODIDE_URL}pyodide.mjs`
            );
            py = await loadPyodide({ indexURL: PYODIDE_URL });
            py.runPython(FRAMEWORK);
            self.postMessage({ type: "ready" });
        } catch (err) {
            self.postMessage({ type: "initError", error: String(err) });
        }
        return;
    }

    if (msg.type === "prime") {
        py.globals.set("__src", msg.src);
        const err = py.runPython("__prime(__src)");
        self.postMessage({ type: "primed", compileError: err || null });
        return;
    }

    if (msg.type === "case") {
        py.globals.set("__fn", msg.fnName || "");
        py.globals.set("__isc", !!msg.isClass);
        py.globals.set("__in", msg.input);
        py.globals.set("__exp", msg.expected);
        py.globals.set("__tl", msg.timeLimitMs || 0);
        py.globals.set("__ml", msg.memLimitMb || 0);
        const out = py.runPython("__grade_one(__fn, __isc, __in, __exp, __tl, __ml)");
        self.postMessage({ type: "result", result: JSON.parse(out) });
        return;
    }
};

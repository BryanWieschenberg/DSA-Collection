const PYODIDE_VERSION = "0.27.7";
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

const PREAMBLE = `
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Optional, Union, Any, Callable, Deque
import collections, heapq, math, bisect, itertools, functools, re, string
from collections import defaultdict, deque, Counter, OrderedDict
from heapq import heappush, heappop, heapify, heappushpop, heapreplace, nlargest, nsmallest
from bisect import bisect_left, bisect_right, insort
from math import sqrt, ceil, floor, gcd, inf, nan
from functools import lru_cache, cache, reduce

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class QuadNode:
    def __init__(self, val=False, isLeaf=False, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
`;

const FRAMEWORK =
    String.raw`
import sys, io, json, traceback, time, tracemalloc, re as __re

__USER = {}

class __Self:
    pass

# ── Container builders ──

def __mk_L(arr):
    if not arr:
        return None
    dummy = ListNode()
    curr = dummy
    for v in arr:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

def __mk_T(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    pos = 1
    while q and pos < len(arr):
        node = q.popleft()
        if pos < len(arr) and arr[pos] is not None:
            node.left = TreeNode(arr[pos])
            q.append(node.left)
        pos += 1
        if pos < len(arr) and arr[pos] is not None:
            node.right = TreeNode(arr[pos])
            q.append(node.right)
        pos += 1
    return root

def __mk_Q(arr):
    if not arr:
        return None
    root = QuadNode(bool(arr[0][1]), bool(arr[0][0]))
    q = deque([root])
    pos = 1
    while q:
        parent = q.popleft()
        if not parent.isLeaf:
            for corner in ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']:
                if pos < len(arr) and arr[pos] is not None:
                    child = QuadNode(bool(arr[pos][1]), bool(arr[pos][0]))
                    setattr(parent, corner, child)
                    q.append(child)
                pos += 1
    return root

def __mk_I(arr):
    root = TrieNode()
    for word in arr:
        curr = root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.end = True
    return root

def __mk_G(arr):
    if not arr:
        return None
    nodes = {i + 1: GraphNode(val=i + 1) for i in range(len(arr))}
    for i, neighbors in enumerate(arr):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]

# ── Container serializers ──

def __arr_L(head):
    if head is None:
        return []
    res = []
    seen = set()
    curr = head
    while curr and id(curr) not in seen:
        seen.add(id(curr))
        res.append(curr.val)
        curr = curr.next
    return res

def __arr_T(root):
    if root is None:
        return []
    res = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    while res and res[-1] is None:
        res.pop()
    return res

def __arr_Q(root):
    if root is None:
        return []
    res = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            res.append([int(node.isLeaf), int(node.val)])
            if not node.isLeaf:
                q.append(node.topLeft)
                q.append(node.topRight)
                q.append(node.bottomLeft)
                q.append(node.bottomRight)
        else:
            res.append(None)
    while res and res[-1] is None:
        res.pop()
    return res

def __arr_I(root):
    if root is None:
        return []
    words = []
    def dfs(node, path):
        if node.end:
            words.append("".join(path))
        for ch in sorted(node.children):
            path.append(ch)
            dfs(node.children[ch], path)
            path.pop()
    dfs(root, [])
    return words

def __arr_G(node):
    if node is None:
        return []
    visited = set()
    q = deque([node])
    nodes = {}
    while q:
        curr = q.popleft()
        if curr.val not in visited:
            visited.add(curr.val)
            nodes[curr.val] = curr
            for nb in curr.neighbors:
                if nb.val not in visited:
                    q.append(nb)
    mx = max(nodes.keys()) if nodes else 0
    adj = []
    for i in range(1, mx + 1):
        if i in nodes:
            adj.append(sorted([n.val for n in nodes[i].neighbors]))
        else:
            adj.append([])
    return adj

# ── Normalize ──

def __normalize(v):
    if isinstance(v, ListNode):
        return __arr_L(v)
    if isinstance(v, TreeNode):
        return __arr_T(v)
    if isinstance(v, QuadNode):
        return __arr_Q(v)
    if isinstance(v, TrieNode):
        return __arr_I(v)
    if isinstance(v, GraphNode):
        return __arr_G(v)
    if isinstance(v, list):
        return [__normalize(x) for x in v]
    if isinstance(v, tuple):
        return tuple(__normalize(x) for x in v)
    return v

# ── Preprocessor: X[...] → __mk_X([...]) ──

def __preprocess(s):
    out = []
    i = 0
    n = len(s)
    qch = None
    while i < n:
        ch = s[i]
        if qch:
            out.append(ch)
            if ch == qch and (i == 0 or s[i - 1] != chr(92)):
                qch = None
            i += 1
            continue
        if ch in ('"', "'"):
            qch = ch
            out.append(ch)
            i += 1
            continue
        if ch in 'LTQIG' and i + 1 < n and s[i + 1] == '[':
            if i > 0 and (s[i - 1].isalnum() or s[i - 1] == '_'):
                out.append(ch)
                i += 1
                continue
            j = i + 1
            depth = 0
            while j < n:
                if s[j] == '[':
                    depth += 1
                elif s[j] == ']':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            inner = s[i + 1:j + 1]
            out.append("__mk_" + ch + "(" + inner + ")")
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)

# ── Eval globals ──

__EVAL_G = {
    "true": True, "false": False, "null": None,
    "__mk_L": __mk_L, "__mk_T": __mk_T, "__mk_Q": __mk_Q,
    "__mk_I": __mk_I, "__mk_G": __mk_G,
}

# ── Formatting ──

def __fmt(v):
    if isinstance(v, ListNode):
        return "L" + __fmt(__arr_L(v))
    if isinstance(v, TreeNode):
        return "T" + __fmt(__arr_T(v))
    if isinstance(v, QuadNode):
        return "Q" + __fmt(__arr_Q(v))
    if isinstance(v, TrieNode):
        return "I" + __fmt(__arr_I(v))
    if isinstance(v, GraphNode):
        return "G" + __fmt(__arr_G(v))
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

# ── Parsing ──

def __parse(s):
    s_pp = __preprocess(s.strip())
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return eval(s_pp, dict(__EVAL_G))
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
            if ch == quote and prev != "\\":
                quote = None
        elif ch in "\"'":
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

__assign_re = __re.compile(r"^\s*[A-Za-z_]\w*\s*=(?!=)")

def __args_from(input_str):
    pp = __preprocess(input_str)
    parts = __split_top(pp)
    if parts and all(__assign_re.match(p) for p in parts):
        ns = {}
        try:
            for p in parts:
                exec(p.strip(), dict(__EVAL_G), ns)
            if ns:
                return list(ns.values())
        except Exception:
            pass
    if parts:
        return [__parse(p.strip()) for p in parts]
    return [__parse(pp)]
` +
    `
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
        pp = __preprocess(input_str)
        ops = eval("[" + pp + "]", dict(__EVAL_G))
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
        nr = __normalize(result)
        ne = __normalize(expected)
        try:
            ok = nr == ne
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
            const { loadPyodide } = await import(/* @vite-ignore */ `${PYODIDE_URL}pyodide.mjs`);
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

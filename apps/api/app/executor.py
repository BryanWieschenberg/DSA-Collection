import os
import sys
sys.setrecursionlimit(200000)
import io
import time
import tracemalloc
import traceback
import inspect
import resource
from typing import List, Optional, Dict, Tuple, Set, Union
from collections import deque, defaultdict, Counter

from app.dsa import (
    ListNode,
    TreeNode,
    TrieNode,
    preprocess_input,
    EVAL_GLOBALS,
    args_from,
    parse_val,
    normalize_val,
    fmt_val_truncated,
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
    ops = None
    constructor_args = None
    buf = io.StringIO()
    sys.stdout = buf

    class MountainArray:
        def __init__(self, arr):
            self.arr = arr
            self.calls = 0

        def get(self, index: int) -> int:
            self.calls += 1
            if self.calls > 100:
                raise RuntimeError("Too many calls to MountainArray.get")
            return self.arr[index]

        def length(self) -> int:
            return len(self.arr)

    class Node:
        def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
            self.val = int(x)
            self.next = next
            self.random = random

    def mk_random_list(arr):
        if not arr:
            return None
        nodes = [Node(val) for val, _ in arr]
        for i, (_, rand_idx) in enumerate(arr):
            if i + 1 < len(nodes):
                nodes[i].next = nodes[i + 1]
            if rand_idx is not None:
                nodes[i].random = nodes[rand_idx]
        return nodes[0]

    def arr_random_list(head):
        if not head:
            return []
        nodes = []
        curr = head
        node_to_idx = {}
        idx = 0
        while curr:
            nodes.append(curr)
            node_to_idx[id(curr)] = idx
            curr = curr.next
            idx += 1
        res = []
        for node in nodes:
            rand_idx = node_to_idx[id(node.random)] if node.random and id(node.random) in node_to_idx else None
            res.append([node.val, rand_idx])
        return res

    ns = {
        "ListNode": ListNode,
        "TreeNode": TreeNode,
        "TrieNode": TrieNode,
        "Node": Node,
        "List": List,
        "Optional": Optional,
        "Dict": Dict,
        "Tuple": Tuple,
        "Set": Set,
        "Union": Union,
        "deque": deque,
        "defaultdict": defaultdict,
        "Counter": Counter,
        "math": __import__("math"),
        "collections": __import__("collections"),
        "heapq": __import__("heapq"),
        "bisect": __import__("bisect"),
        "itertools": __import__("itertools"),
        "functools": __import__("functools"),
        "re": __import__("re"),
        "string": __import__("string"),
        "MountainArray": MountainArray,
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
            if (
                len(ops) == 1
                and isinstance(ops[0], list)
                and ops[0]
                and isinstance(ops[0][0], list)
            ):
                ops = ops[0]
            cls = ns.get(ops[0][0])
            if cls is None:
                raise RuntimeError(f"Class '{ops[0][0]}' is not defined.")
            if (
                ops[0][0] == "Codec"
                and cls is not None
                and not hasattr(cls, "encode_and_decode")
            ):
                cls.encode_and_decode = lambda self, strs: self.decode(
                    self.encode(strs)
                )

            tracemalloc.start()
            t0 = time.perf_counter()

            def parse_arg(v):
                if (
                    isinstance(v, str)
                    and len(v) >= 3
                    and v[0] in "LTI"
                    and v[1] == "["
                    and v[-1] == "]"
                ):
                    return parse_val(v)
                if isinstance(v, list):
                    return [parse_arg(x) for x in v]
                if isinstance(v, tuple):
                    return tuple(parse_arg(x) for x in v)
                if isinstance(v, dict):
                    return {k: parse_arg(val) for k, val in v.items()}
                return v

            constructor_args = (
                ops[0][1]
                if len(ops[0]) > 1 and isinstance(ops[0][1], list)
                else ops[0][1:]
            )
            constructor_args = [parse_arg(x) for x in constructor_args]
            obj = cls(*constructor_args)
            out = [None]
            for op in ops[1:]:
                method_args = (
                    op[1] if len(op) > 1 and isinstance(op[1], list) else op[1:]
                )
                method_args = [parse_arg(x) for x in method_args]
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

            if fn_name == "guessNumber" and len(args) >= 2:
                pick = args[1]

                def guess(num: int) -> int:
                    if num > pick:
                        return -1
                    elif num < pick:
                        return 1
                    return 0

                ns["guess"] = guess
                args = [args[0]]
            elif fn_name == "findInMountainArray" and len(args) >= 2:
                args[1] = ns["MountainArray"](args[1])
            elif fn_name == "hasCycle" and len(args) >= 2:
                head = args[0]
                pos = args[1]
                if pos != -1 and head:
                    curr = head
                    pos_node = None
                    idx = 0
                    while curr.next:
                        if idx == pos:
                            pos_node = curr
                        curr = curr.next
                        idx += 1
                    if idx == pos:
                        pos_node = curr
                    curr.next = pos_node
                args = [head]
            elif fn_name == "copyRandomList" and len(args) >= 1:
                head_node = mk_random_list(args[0])
                args = [head_node]
            elif fn_name == "lowestCommonAncestor" and len(args) >= 3:
                root_node = args[0]
                p_val = args[1]
                q_val = args[2]
                def find_node(node, val):
                    if not node: return None
                    if node.val == val: return node
                    return find_node(node.left, val) or find_node(node.right, val)
                if not isinstance(p_val, TreeNode) and root_node:
                    args[1] = find_node(root_node, p_val)
                if not isinstance(q_val, TreeNode) and root_node:
                    args[2] = find_node(root_node, q_val)

            sig = inspect.signature(fn)
            params = list(sig.parameters.keys())

            tracemalloc.start()
            t0 = time.perf_counter()

            if params and params[0] == "self":

                class DummySelf:
                    pass

                original_fn = fn

                def wrapped_fn(*f_args, **f_kwargs):
                    if not f_args or not isinstance(f_args[0], DummySelf):
                        return original_fn(DummySelf(), *f_args, **f_kwargs)
                    return original_fn(*f_args, **f_kwargs)

                ns[fn_name] = wrapped_fn
                result = wrapped_fn(DummySelf(), *args)
            else:
                result = fn(*args)

            if fn_name == "copyRandomList":
                result = arr_random_list(result)

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
        
        is_random_node = False
        if is_class and ops and ops[0][0] == "Solution" and any(op[0] == "getRandom" for op in ops[1:]):
            is_random_node = True

        if is_random_node:
            try:
                curr = constructor_args[0]
                vals = []
                while curr:
                    vals.append(curr.val)
                    curr = curr.next
                val_set = set(vals)

                ok = True
                if len(nr) != len(ne):
                    ok = False
                else:
                    if nr[0] is not None:
                        ok = False
                    for val in nr[1:]:
                        if val not in val_set:
                            ok = False
                            break
                    if ok and len(val_set) > 1 and len(nr) > 10:
                        returned_vals = set(nr[1:])
                        if len(returned_vals) == 1:
                            ok = False
            except Exception:
                ok = False
        else:
            try:
                ok = nr == ne
            except Exception:
                ok = False

        raw_output = fmt_val_truncated(result)
        if len(raw_output) > 50000:
            raw_output = raw_output[:50000] + "... [Output Truncated]"

        base.update(
            {"status": "AC" if ok else "WA", "error": None, "output": raw_output}
        )

    return base

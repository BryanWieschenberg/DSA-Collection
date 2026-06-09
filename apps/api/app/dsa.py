import json
import re
from collections import deque


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


def mk_L(arr):
    if not arr:
        return None
    dummy = ListNode()
    curr = dummy
    for v in arr:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def mk_T(arr):
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


def mk_I(arr):
    root = TrieNode()
    for word in arr:
        curr = root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.end = True
    return root


def arr_L(head):
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


def arr_T(root):
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


def arr_I(root):
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


def normalize_val(v):
    name = v.__class__.__name__
    if name == "ListNode":
        return arr_L(v)
    if name == "TreeNode":
        return arr_T(v)
    if name == "TrieNode":
        return arr_I(v)
    if isinstance(v, list):
        return [normalize_val(x) for x in v]
    if isinstance(v, tuple):
        return tuple(normalize_val(x) for x in v)
    return v


def preprocess_input(s):
    if not re.search(r"(?<![A-Za-z0-9_])[LTI]\[", s):
        return s

    out = []
    i = 0
    n = len(s)
    qch = None
    escaped = False
    while i < n:
        ch = s[i]
        if qch:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == qch:
                qch = None
            i += 1
            continue
        if ch in ('"', "'"):
            qch = ch
            escaped = False
            out.append(ch)
            i += 1
            continue
        if ch in "LTI" and i + 1 < n and s[i + 1] == "[":
            if i > 0 and (s[i - 1].isalnum() or s[i - 1] == "_"):
                out.append(ch)
                i += 1
                continue
            j = i + 1
            depth = 0
            while j < n:
                if s[j] == "[":
                    depth += 1
                elif s[j] == "]":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            inner = s[i + 1 : j + 1]
            out.append("__mk_" + ch + "(" + inner + ")")
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


EVAL_GLOBALS = {
    "true": True,
    "false": False,
    "null": None,
    "__mk_L": mk_L,
    "__mk_T": mk_T,
    "__mk_I": mk_I,
}


def fmt_val(v):
    name = v.__class__.__name__
    if name == "ListNode":
        return "L" + fmt_val(arr_L(v))
    if name == "TreeNode":
        return "T" + fmt_val(arr_T(v))
    if name == "TrieNode":
        return "I" + fmt_val(arr_I(v))
    if v is True:
        return "True"
    if v is False:
        return "False"
    if v is None:
        return "None"
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, list):
        return "[" + ", ".join(fmt_val(x) for x in v) + "]"
    if isinstance(v, tuple):
        return "(" + ", ".join(fmt_val(x) for x in v) + ")"
    if isinstance(v, dict):
        return (
            "{"
            + ", ".join(json.dumps(k) + ": " + fmt_val(val) for k, val in v.items())
            + "}"
        )
    try:
        return json.dumps(v)
    except Exception:
        return repr(v)


def parse_val(s):
    if not s or not s.strip():
        return None
    s_pp = preprocess_input(s.strip())
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        return eval(s_pp, dict(EVAL_GLOBALS))
    except Exception:
        return s


def split_top(s):
    parts = []
    depth = 0
    quote = None
    escaped = False
    start = 0
    for idx, ch in enumerate(s):
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            escaped = False
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(s[start:idx])
            start = idx + 1

    last_part = s[start:]
    if last_part.strip():
        parts.append(last_part)
    return parts


ASSIGN_RE = re.compile(r"^\s*[A-Za-z_]\w*\s*=(?!=)")


def args_from(input_str):
    pp = preprocess_input(input_str)
    parts = split_top(pp)
    if parts and all(ASSIGN_RE.match(p) for p in parts):
        vals = []
        try:
            for p in parts:
                name, val_str = p.split("=", 1)
                vals.append(parse_val(val_str.strip()))
            return vals
        except Exception:
            pass
    if parts:
        return [parse_val(p.strip()) for p in parts]
    return [parse_val(pp)]


def fmt_val_truncated(v):
    name = v.__class__.__name__
    if name == "ListNode":
        return "L" + fmt_val_truncated(arr_L(v))
    if name == "TreeNode":
        return "T" + fmt_val_truncated(arr_T(v))
    if name == "TrieNode":
        return "I" + fmt_val_truncated(arr_I(v))
    if v is True:
        return "True"
    if v is False:
        return "False"
    if v is None:
        return "None"
    if isinstance(v, str):
        if len(v) > 30:
            return f'"{v[:10]}...{v[-10:]}" (len={len(v)})'
        return json.dumps(v)
    if isinstance(v, list):
        if len(v) > 30:
            parts = (
                [fmt_val_truncated(x) for x in v[:5]]
                + ["..."]
                + [fmt_val_truncated(x) for x in v[-5:]]
            )
            return f"[{', '.join(parts)}] (len={len(v)})"
        return "[" + ", ".join(fmt_val_truncated(x) for x in v) + "]"
    if isinstance(v, tuple):
        if len(v) > 30:
            parts = (
                [fmt_val_truncated(x) for x in v[:5]]
                + ["..."]
                + [fmt_val_truncated(x) for x in v[-5:]]
            )
            return f"({', '.join(parts)}) (len={len(v)})"
        return "(" + ", ".join(fmt_val_truncated(x) for x in v) + ")"
    if isinstance(v, dict):
        if len(v) > 30:
            items = list(v.items())
            parts = (
                [f"{json.dumps(k)}: {fmt_val_truncated(val)}" for k, val in items[:5]]
                + ["..."]
                + [
                    f"{json.dumps(k)}: {fmt_val_truncated(val)}"
                    for k, val in items[-5:]
                ]
            )
            return f"{{{', '.join(parts)}}} (len={len(v)})"
        return (
            "{"
            + ", ".join(
                json.dumps(k) + ": " + fmt_val_truncated(val) for k, val in v.items()
            )
            + "}"
        )
    try:
        return json.dumps(v)
    except Exception:
        return repr(v)


def truncate_str_repr(s):
    if not s:
        return s
    s = s.strip()
    pp = preprocess_input(s)
    parts = split_top(pp)
    out_parts = []
    for part in parts:
        part = part.strip()
        if "=" in part:
            try:
                name, val_str = part.split("=", 1)
                val = parse_val(val_str.strip())
                out_parts.append(f"{name.strip()} = {fmt_val_truncated(val)}")
            except Exception:
                out_parts.append(part)
        else:
            try:
                val = parse_val(part)
                out_parts.append(fmt_val_truncated(val))
            except Exception:
                out_parts.append(part)
    return ", ".join(out_parts)

from typing import List, Optional, Dict, Hashable, Union
from collections import deque
from math import floor, ceil
from random import shuffle
from time import perf_counter
from signal import signal, alarm, SIGALRM
from resource import setrlimit, RLIMIT_AS, getrusage, RUSAGE_SELF

MAX_LEN = 10
HEAD = 3
TAIL = 3

class TimeLimitExceeded(Exception):
    pass

class Tester:
    def __init__(self):
        self.hl = ListHelper()
        self.ht = TreeHelper()
        self.hq = QuadTreeHelper()
        self.hi = TrieHelper()
        self.hg = GraphHelper()
        self.hv = IntervalHelper()

    def _timeout_handler(self, signum, frame):
        raise TimeLimitExceeded()
    
    def _set_memory_limit(self, mb):
        bytes = mb * 1024 * 1024
        setrlimit(RLIMIT_AS, (bytes, bytes))

    def _eq(self, a, b):
        if isinstance(a, ListNode) and isinstance(b, ListNode):
            return self.hl.print(a, verbose=False) == self.hl.print(b, verbose=False)
        elif isinstance(a, TreeNode) and isinstance(b, TreeNode):
            return self.ht.print(a, verbose=False) == self.ht.print(b, verbose=False)
        elif isinstance(a, QuadTreeNode) and isinstance(b, QuadTreeNode):
            return self.hq.print(a, verbose=False) == self.hq.print(b, verbose=False)
        elif isinstance(a, TrieNode) and isinstance(b, TrieNode):
            return self.hi.print(a, verbose=False) == self.hi.print(b, verbose=False)
        elif isinstance(a, Node) and isinstance(b, Node):
            return self.hg.print(a, verbose=False) == self.hg.print(b, verbose=False)
        elif isinstance(a, Interval) and isinstance(b, Interval):
            return a.start == b.start and a.end == b.end
        elif isinstance(a, list) and isinstance(b, list) and all(isinstance(x, Interval) for x in a) and all(isinstance(y, Interval) for y in b):
            return self.hv.print(a, verbose=False) == self.hv.print(b, verbose=False)
        return a == b

    def _fmt(self, x):
        if isinstance(x, str):
            if len(x) > MAX_LEN:
                return f"{x[:3]}...{x[-3:]}"
            return x

        if isinstance(x, list):
            if not x:
                return "[]"
            if len(x) > MAX_LEN:
                return f"l{str(x[:HEAD])[:-1]}, ..., {str(x[-TAIL:])[1:]}(len={len(x)})"
            return str(x)
        
        if isinstance(x, ListNode):
            return self.hl.print(x, verbose=False)
        elif isinstance(x, TreeNode):
            return self.ht.print(x, verbose=False)
        elif isinstance(x, QuadTreeNode):
            return self.hq.print(x, verbose=False)
        elif isinstance(x, TrieNode):
            return self.hi.print(x, verbose=False)
        elif isinstance(x, Node):
            return self.hg.print(x, verbose=False)
        elif isinstance(x, Interval):
            return self.hv.print(x, verbose=False)

        if isinstance(x, list) and x and all(isinstance(item, Interval) for item in x):
            return self.hv.print(x, verbose=False)

        return str(x)
    
    def test(self, fn: callable, tests: list[tuple], time: int = 1, space: int = 256, verbose: bool = True) -> None:
        passed = 0
        total = len(tests)
        green, red, blue, bold, reset = "\033[92m", "\033[91m", "\033[94m", "\033[1m", "\033[0m"
        lines = [(f"{blue}Results for {bold}{fn.__name__}{reset}:")]

        signal(SIGALRM, self._timeout_handler)
        self._set_memory_limit(space)
        start_time = perf_counter()

        for (args, expected) in tests:
            if not isinstance(args, tuple):
                args = (args,)

            arg_display = f"({self._fmt(args[0])})" if len(args) == 1 else f"({', '.join(str(self._fmt(a)) for a in args)})"

            try:
                alarm(time)
                result = fn(*args)
            except TimeLimitExceeded:
                lines.append(f"{red}❌ Time Limit Exceeded on {arg_display}{reset}")
                print("\n".join(lines))
                return
            except MemoryError:
                lines.append(f"{red}❌ Memory Limit Exceeded on {arg_display}{reset}")
                print("\n".join(lines))
                return
            finally:
                alarm(0)

            ok = self._eq(result, expected)
            rfmt = self._fmt(result)
            efmt = self._fmt(expected)

            if ok:
                if verbose: lines.append(f"  > ✅ {arg_display} == {efmt}")
                passed += 1
            else:
                if verbose: lines.append(f"  > ❌ {arg_display}\n       - Received {rfmt}\n       - Expected {efmt}")

        end_time = perf_counter()
        elapsed = end_time - start_time
        peak_mb = getrusage(RUSAGE_SELF).ru_maxrss / 1024

        if passed == total:
            lines.append(
                f"{green}✅ {total}/{total} tests passed{reset}  "
                f"{blue}Time: {elapsed:.3f} seconds  Space: {peak_mb:.1f} MB"
            )
        else:
            lines.append(f"{red}❌ {passed}/{total} tests passed{reset}")
        
        print("\n".join(lines))

    def testcls(self, cls: type, init_args: tuple, steps: list[tuple], time: int = 1, space: int = 256, verbose: bool = True) -> None:
        if not isinstance(init_args, tuple):
            init_args = (init_args,)

        instance = cls(*init_args)
        passed = 0
        total = len(steps)
        green, red, blue, bold, reset = "\033[92m", "\033[91m", "\033[94m", "\033[1m", "\033[0m"
        clsname = instance.__class__.__name__
        lines = [(f"{blue}Results for {bold}{clsname}{reset}:")]

        signal(SIGALRM, self._timeout_handler)
        self._set_memory_limit(space)
        start_time = perf_counter()

        for method_name, args, expected in steps:
            if not isinstance(args, tuple):
                args = (args,)

            method = getattr(instance, method_name)
            arg_display = f"({self._fmt(args[0])})" if len(args) == 1 else f"({', '.join(str(self._fmt(a)) for a in args)})"
            call_str = f"{method_name}{arg_display}"

            try:
                alarm(time)
                result = method(*args)
            except TimeLimitExceeded:
                lines.append(f"{red}❌ Time Limit Exceeded on {arg_display}{reset}")
                print("\n".join(lines))
                return
            except MemoryError:
                lines.append(f"{red}❌ Memory Limit Exceeded on {arg_display}{reset}")
                print("\n".join(lines))
                return
            finally:
                alarm(0)

            ok = self._eq(result, expected)
            rfmt = self._fmt(result)
            efmt = self._fmt(expected)

            if ok:
                if verbose: lines.append(f"  > ✅ {call_str} == {efmt}")
                passed += 1
            else:
                if verbose: lines.append(f"  > ❌ {call_str}\n       - Received {rfmt}\n       - Expected {efmt}")

        end_time = perf_counter()
        elapsed = end_time - start_time
        peak_mb = getrusage(RUSAGE_SELF).ru_maxrss / 1024

        if passed == total:
            lines.append(
                f"{green}✅ {total}/{total} tests passed{reset}  "
                f"{blue}Time: {elapsed:.3f} seconds  Space: {peak_mb:.1f} MB"
            )
        else:
            lines.append(f"{red}❌ {passed}/{total} tests passed{reset}")
        
        print("\n".join(lines))

class ListNode:
    def __init__(self, val=0, next=None, prev=None, key=None, cycle=None, random=None):
        self.val = val
        self.next = next
        self.prev = prev
        self.key = key
        self.cycle = cycle
        self.random = random

class ListHelper:
    @staticmethod
    def to(values: List, cycle: Optional[int] = None) -> Optional[ListNode]:
        if not values:
            return None

        if isinstance(values[0], int):
            nodes = [ListNode(val=v) for v in values]
        else:
            nodes = [ListNode(val=pair[0]) for pair in values]

        for i in range(len(nodes)-1):
            nodes[i].next = nodes[i + 1]

        if cycle is not None and 0 <= cycle < len(nodes):
            nodes[-1].next = nodes[cycle]
            nodes[-1].cycle = nodes[cycle]

        if isinstance(values[0], list):
            for i, pair in enumerate(values):
                randID = pair[1]
                if randID is None:
                    continue
                if 0 <= randID < len(nodes):
                    nodes[i].random = nodes[randID]
                else:
                    raise ValueError(f"Invalid random index {randID} for node {i}")

        return nodes[0]

    @staticmethod
    def print(head: Optional[ListNode], verbose=True) -> str:
        if not head:
            if verbose: print("< Empty list >")
            return "l[]"
        
        output = ""
        res = []
        curr = head
        while curr:
            msg = (
                f"{curr.val},{curr.random.val}" if curr.random else
                f"{curr.val} -> {curr.cycle.val}.." if curr.cycle else
                f"{curr.val}"
            )
            if curr.random:
                res.append([curr.val, curr.random.val])
            elif curr.cycle:
                res.extend([curr.val, curr.cycle.val])
            else:
                res.append(curr.val)
            tail = " -> " if curr.next and not curr.cycle else ""
            output += msg + tail
            if curr.cycle: break
            curr = curr.next

        if verbose: print(output)
        if curr is not None and curr.cycle:
            return f"l{str(res)[:-1]}...]"
        if len(res) > MAX_LEN:
            return f"l{str(res[:HEAD])[:-1]}, ..., {str(res[-TAIL:])[1:]}(len={len(res)})"
        return f"l{str(res)}"

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class TreeHelper:
    @staticmethod
    def to(values: List):
        if not values:
            return None

        nodes = [TreeNode(v) if v is not None else None for v in values]

        for i in range(len(values)):
            node = nodes[i]
            if node is None:
                continue

            li = 2 * i + 1
            ri = 2 * i + 2

            if li < len(values):
                node.left = nodes[li]
            if ri < len(values):
                node.right = nodes[ri]

        return nodes[0]

    @staticmethod
    def print(root, verbose=True) -> str:
        def getHeight(node):
            if node is None:
                return 0
            return 1 + max(getHeight(node.left), getHeight(node.right))

        def inorder(root):
            tmp = []

            def dfs(node, depth=0, connector="", parent=None):
                if not node:
                    return
                dfs(node.left, depth + 1, 'L', node)
                tmp.append([None, node, depth, connector, parent])
                dfs(node.right, depth + 1, 'R', node)

            dfs(root, 0, "", None)

            for i, it in enumerate(tmp):
                it[0] = i

            idx = {it[1]: it[0] for it in tmp}

            vals = [(it[0], it[1].val, it[2], it[3], (idx[it[4]] if it[4] is not None else None)) for it in tmp]
            return vals

        depth = getHeight(root)
        vals = inorder(root)
        if not vals:
            if verbose: print("< Empty tree >")
            return "t[]"
        
        lines = ["" for _ in range(depth * 2 - 1)]
        offsets = [0] * (depth * 2 - 1)
        positions = {}

        for i, (id, val, d, connector_sign, _) in enumerate(vals):
            text = str(val)
            w = len(text)

            line_index = d * 2
            
            lsp, rsp = 0, 0
            if i-1 >= 0 and vals[i-1][2] == d-1:
                lsp = 1
            elif i+1 < len(vals) and vals[i+1][2] == d-1:
                rsp = 1

            lines[line_index] += " " * (offsets[line_index] - len(lines[line_index]) + lsp) + text + " " * rsp
            offsets[line_index] = len(lines[line_index])

            if connector_sign == 'L':
                positions[id] = offsets[line_index] - rsp - 1
            else:
                positions[id] = offsets[line_index] - w - rsp

            for i in range(depth):
                li = i * 2
                if li != line_index:
                    offsets[li] += w + lsp + rsp
        for (id, val, d, connector, cid) in vals:
            if cid is None:
                continue
            ppos = positions[cid] + (len(str(vals[cid][1])) - 1 if connector == 'R' else -len(str(vals[cid][1])) // 2)
            cpos = positions[id]
            mid = (ppos + cpos) / 2
            mid = ceil(mid) if connector == 'L' else floor(mid)
            connectorLine = d * 2 - 1
            lines[connectorLine] += " " * (mid - len(lines[connectorLine])) + ('/' if connector == 'L' else '\\')

        output = ""
        for i in range(len(lines)):
            output += lines[i]
            if i + 1 < len(lines):
                output += "\n"

        q = deque([root])
        res = []

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

        if verbose: print(output)
        if len(res) > MAX_LEN:
            return f"t{str(res[:HEAD])[:-1]}, ..., {str(res[-TAIL:])[1:]}(len={len(res)})"
        return f"t{str(res)}"

class QuadTreeNode:
    def __init__(self, val, isLeaf, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight

class QuadTreeHelper:
    @staticmethod
    def to(arr):
        if not arr:
            return None

        def make(node):
            isLeaf, val = node
            return QuadTreeNode(val, bool(isLeaf))

        root_info = arr[0]
        root = make(root_info)

        q = deque([root])
        i = 1

        while q and i < len(arr):
            node = q.popleft()

            if node.isLeaf:
                continue

            tl = make(arr[i]); i += 1
            tr = make(arr[i]); i += 1
            bl = make(arr[i]); i += 1
            br = make(arr[i]); i += 1

            node.topLeft = tl
            node.topRight = tr
            node.bottomLeft = bl
            node.bottomRight = br

            if not tl.isLeaf: q.append(tl)
            if not tr.isLeaf: q.append(tr)
            if not bl.isLeaf: q.append(bl)
            if not br.isLeaf: q.append(br)

        return root

    @staticmethod
    def print(root, verbose=True) -> str:
        if root is None:
            if verbose: print("< Empty quad tree >")
            return "q[]"

        out = []
        q = [root]

        while q:
            node = q.pop(0)
            out.append([1 if node.isLeaf else 0, 1 if node.val else 0])

            if not node.isLeaf:
                q.append(node.topLeft)
                q.append(node.topRight)
                q.append(node.bottomLeft)
                q.append(node.bottomRight)

        if verbose: print(out)
        if len(out) > MAX_LEN:
            return f"q{str(out[:HEAD])[:-1]}, ..., {str(out[-TAIL:])[1:]}(len={len(out)})"
        return f"q{str(out)}"

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.word = None

class TrieHelper:
    @staticmethod
    def to(words: List):
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.end = True
        return root
  
    @staticmethod
    def print(root, verbose=True):
        def dfs(node, prefix, indent, is_last, is_root_child=False):
            while len(node.children) == 1 and not node.end:
                char = next(iter(node.children))
                prefix += char
                node = node.children[char]
            
            if is_root_child:
                lines.append(prefix)
                new_indent = ""
            else:
                connector = "└── " if is_last else "├── "
                lines.append(indent + connector + prefix)
                continuation = "    " if is_last else "│   "
                new_indent = indent + continuation
            
            if node.children:
                children = sorted(node.children.keys())
                for i, char in enumerate(children):
                    child_is_last = (i == len(children) - 1)
                    dfs(node.children[char], char, new_indent, child_is_last, False)

        if not root:
            if verbose: print("< Empty trie >")
            return "i[]"

        lines = []
        children = sorted(root.children.keys())
        for i, char in enumerate(children):
            is_last = (i == len(children) - 1)
            dfs(root.children[char], char, "", is_last, True)

        out = "\n".join(lines)
        if verbose: print(out)
        if len(out) > MAX_LEN:
            return f"i{str(out[:HEAD])[:-1]}, ..., {str(out[-TAIL:])[1:]}(len={len(out)})"
        return f"i{str(out)}"

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class GraphHelper:
    # Takes in an adjacency list or node-named dict
    # Supports weighted and unweighted graphs
    @staticmethod
    def to(adjList:
        List[List[Union[int, tuple[int, float]]]] |
        Dict[Hashable, List[Union[int, tuple[Hashable, float]]]]
    ) -> "Node | None":
        if not len(adjList):
            return None

        if isinstance(adjList, dict):
            nodes = {key: Node(key) for key in adjList.keys()}

            for key, neighbors in adjList.items():
                node = nodes[key]
                for entry in neighbors:
                    if isinstance(entry, list) and len(entry) == 2:
                        neighbor_id, weight = entry
                    else:
                        neighbor_id, weight = entry, None

                    if neighbor_id not in nodes:
                        nodes[neighbor_id] = Node(neighbor_id)

                    if weight is None:
                        node.neighbors.append(nodes[neighbor_id])
                    else:
                        node.neighbors.append([nodes[neighbor_id], weight])

            return nodes[next(iter(adjList))]

        elif isinstance(adjList, list):
            nodes = {i + 1: Node(i + 1) for i in range(len(adjList))}

            for i, neighbors in enumerate(adjList):
                node = nodes[i + 1]
                for entry in neighbors:
                    if isinstance(entry, list) and len(entry) == 2:
                        neighbor_id, weight = entry
                    else:
                        neighbor_id, weight = entry, None

                    if weight is None:
                        node.neighbors.append(nodes[neighbor_id])
                    else:
                        node.neighbors.append([nodes[neighbor_id], weight])

            return nodes[1]

        return None

    @staticmethod
    def print(start: Optional[Node], tree=False, verbose=True):
        if not start:
            if verbose: print("< Empty graph >")
            return "g[]"

        lines = []

        if tree:
            def dfs(node, indent, is_last, visited):
                if node in visited:
                    return
                visited.add(node)

                connector = "└── " if is_last else "├── "
                lines.append(indent + connector + str(node.val))

                children = [n for n in node.neighbors if n not in visited]
                for i, child in enumerate(children):
                    is_child_last = (i == len(children) - 1)
                    new_indent = indent + ("    " if is_last else "│   ")
                    dfs(child, new_indent, is_child_last, visited)

            visited = set()
            children = start.neighbors
            lines.append(str(start.val))

            for i, child in enumerate(children):
                is_last = (i == len(children) - 1)
                dfs(child, "", is_last, visited)
        else:
            visited = set()
            queue = [start]
            lines = []
            adj = []

            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)

                neighbors_info = []
                adj_row = []
                for n in current.neighbors:
                    if isinstance(n, list):
                        neighbor_node, weight = n
                        neighbors_info.append(f"[{neighbor_node.val}, {weight}]")
                        adj_row.append([neighbor_node.val, weight])
                        if neighbor_node not in visited:
                            queue.append(neighbor_node)
                    else:
                        neighbors_info.append(str(n.val))
                        adj_row.append(n.val)
                        if n not in visited:
                            queue.append(n)

                lines.append(f"{current.val} -> [{', '.join(neighbors_info)}]")
                adj.append(adj_row)

        out = "\n".join(lines)
        if verbose: print(out)
        if len(adj) > MAX_LEN:
            return f"g{str(adj[:HEAD])[:-1]}, ..., {str(adj[-TAIL:])[1:]}(len={len(adj)})"
        return f"g{str(adj)}"

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class IntervalHelper:
    @staticmethod
    def to(intervals: List[tuple[int]]):
        if not intervals:
            return None

        out = []
        for it in intervals:
            if isinstance(it, tuple) and len(it) == 2:
                out.append(Interval(it[0], it[1]))
            elif isinstance(it, list) and len(it) == 2:
                out.append(Interval(it[0], it[1]))
            else:
                raise ValueError(f"Invalid interval: {it}")
        
        return out

    @staticmethod
    def print(intervals, verbose=True):
        if intervals is None:
            if verbose: print("< Empty interval >")
            return "v[]"

        if isinstance(intervals, Interval):
            intervals = [intervals]

        out = []
        for it in intervals:
            out.append(f"({it.start},{it.end})")

        out = ",".join(out)
        if verbose: print(out)
        if len(out) > MAX_LEN:
            return f"v[\"{str(out[:HEAD])[:-1]}, ..., {str(out[-TAIL:])[1:]}(len={len(out)})\"]"
        return f"v[\"{out}\"]"

class API:
    @staticmethod
    def guess(n: int, pick: int) -> int:
        if n < pick: return 1
        elif n > pick: return -1
        return 0

shuffled_size = 1*10**6
shuffled = list(range(shuffled_size))
shuffle(shuffled)

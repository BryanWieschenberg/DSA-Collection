const EXCLUDED_LABELS = new Set([
    "prerequisites",
    "edges",
    "trust",
    "queries",
    "equations",
    "trips",
    "points",
    "tasks",
    "relations",
    "connections",
]);

function isValidGrid(label, numRows, numCols) {
    if (label && EXCLUDED_LABELS.has(label.toLowerCase())) {
        return false;
    }
    if (numCols === 2) {
        const gridKeywords = [
            "grid",
            "board",
            "matrix",
            "image",
            "rooms",
            "maze",
            "output",
            "expected",
        ];
        const hasGridKeyword = label
            ? gridKeywords.some((kw) => label.toLowerCase().includes(kw))
            : false;
        if (!hasGridKeyword && numRows > 3) {
            return false;
        }
    }
    return true;
}

function extractGrids(val, label = "") {
    const grids = [];

    const isPrimitiveGrid = (arr) => {
        if (!Array.isArray(arr) || arr.length <= 1) return false;
        const firstLen = Array.isArray(arr[0]) ? arr[0].length : -1;
        if (firstLen <= 0) return false;
        return arr.every(
            (row) =>
                Array.isArray(row) &&
                row.length === firstLen &&
                row.every(
                    (cell) =>
                        cell === null ||
                        typeof cell === "number" ||
                        typeof cell === "string" ||
                        typeof cell === "boolean",
                ),
        );
    };

    const traverse = (x, currentLabel) => {
        if (!x) return;
        if (Array.isArray(x)) {
            if (isPrimitiveGrid(x)) {
                if (isValidGrid(currentLabel, x.length, x[0].length)) {
                    grids.push({ label: currentLabel, grid: x });
                    return;
                }
            }
            x.forEach((item, idx) => {
                const itemLabel = currentLabel ? `${currentLabel}[${idx}]` : `${idx}`;
                traverse(item, itemLabel);
            });
        } else if (typeof x === "object") {
            for (const key in x) {
                traverse(x[key], key);
            }
        }
    };

    traverse(val, label);
    return grids;
}

/* eslint-disable react-refresh/only-export-components */
export function parseGrids(inputStr, defaultLabel = "") {
    if (!inputStr) return [];
    const sanitized = inputStr
        .replace(/'/g, '"')
        .replace(/\bTrue\b/g, "true")
        .replace(/\bFalse\b/g, "false")
        .replace(/\bNone\b/g, "null");

    try {
        const parsed = JSON.parse(sanitized);
        return extractGrids(parsed, defaultLabel);
    } catch {
        /* noop */
    }

    const grids = [];
    let i = 0;
    while (i < sanitized.length) {
        if (sanitized[i] === "[" || sanitized[i] === "{") {
            let count = 0;
            const start = i;
            let j = i;
            const openChar = sanitized[i];
            const closeChar = openChar === "[" ? "]" : "}";
            while (j < sanitized.length) {
                if (sanitized[j] === openChar) {
                    count++;
                } else if (sanitized[j] === closeChar) {
                    count--;
                    if (count === 0) {
                        const candidate = sanitized.substring(start, j + 1);
                        try {
                            const parsed = JSON.parse(candidate);
                            let label = defaultLabel;
                            const before = sanitized.substring(0, start).trim();
                            const labelMatch = before.match(/([a-zA-Z_]\w*)\s*=\s*$/);
                            if (labelMatch) {
                                label = labelMatch[1];
                            }
                            grids.push(...extractGrids(parsed, label));
                        } catch {
                            /* noop */
                        }
                        i = j;
                        break;
                    }
                }
                j++;
            }
        }
        i++;
    }
    return grids;
}

export function GridVisualizer({ label, grid }) {
    if (!grid || grid.length === 0 || grid[0].length === 0) return null;
    const numRows = grid.length;
    const numCols = grid[0].length;
    if (numRows < 2 || numRows * numCols < 2) return null;

    const getCellClass = () => {
        return "bg-zinc-800 text-zinc-100 font-bold";
    };

    const isOutputLabel =
        label && (label.toLowerCase() === "output" || label.toLowerCase() === "expected");
    const labelStyle = isOutputLabel ? { color: "#34D399" } : { color: "#E4E4E7" };

    return (
        <div className="flex flex-col items-center mt-0 mb-0.5 select-none">
            {label && (
                <div className="text-xs font-mono mb-0.5 text-center w-full" style={labelStyle}>
                    {label}
                </div>
            )}
            <div className="overflow-auto max-w-full max-h-[350px] border border-zinc-700 bg-zinc-700 p-0 rounded-none">
                <div
                    className="grid gap-px"
                    style={{
                        gridTemplateColumns: `repeat(${numCols}, 36px)`,
                    }}
                >
                    {grid.map((row, r) =>
                        row.map((val, c) => {
                            const bgClass = getCellClass(val);
                            const displayVal =
                                val === 2147483647 ? "∞" : val === null ? "∅" : String(val);
                            return (
                                <div
                                    key={`${r}-${c}`}
                                    className={`w-9 h-9 flex items-center justify-center text-base font-sans rounded-none leading-none text-center p-0 m-0 ${bgClass}`}
                                    title={`Cell (${r}, ${c}): ${val}`}
                                >
                                    {displayVal}
                                </div>
                            );
                        }),
                    )}
                </div>
            </div>
        </div>
    );
}

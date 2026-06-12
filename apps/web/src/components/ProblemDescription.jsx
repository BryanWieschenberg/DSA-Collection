import { useRef, useEffect } from "react";
import { renderMarkdown } from "./RenderMarkdown";
import { compactValue, pythonize, depythonize } from "../lib/appHelpers";
import { GridVisualizer, parseGrids } from "./GridVisualizer";

const VALUE_TOKEN =
    /("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:true|false|null|True|False|None)\b|-?\d+(?:\.\d+)?)/g;

const highlightValue = (text) => {
    if (!text) return text;
    return text.split(VALUE_TOKEN).map((part, i) => {
        if (!part) return null;
        const c = part[0];
        if (c === '"' || c === "'") {
            return (
                <span key={i} style={{ color: "#CE9178" }}>
                    {part}
                </span>
            );
        }
        if (/^(true|false|null|True|False|None)$/.test(part)) {
            return (
                <span key={i} style={{ color: "#569CD6" }}>
                    {part}
                </span>
            );
        }
        if (/^-?\d/.test(part)) {
            return (
                <span key={i} style={{ color: "#B5CEA8" }}>
                    {part}
                </span>
            );
        }
        return part;
    });
};

function parseLevelOrder(arr) {
    if (!arr || arr.length === 0 || arr[0] === null || arr[0] === undefined) return null;
    const root = { val: arr[0], left: null, right: null };
    const queue = [root];
    let i = 1;
    while (queue.length > 0 && i < arr.length) {
        const curr = queue.shift();
        if (i < arr.length) {
            const val = arr[i++];
            if (val !== null && val !== undefined) {
                curr.left = { val, left: null, right: null };
                queue.push(curr.left);
            }
        }
        if (i < arr.length) {
            const val = arr[i++];
            if (val !== null && val !== undefined) {
                curr.right = { val, left: null, right: null };
                queue.push(curr.right);
            }
        }
    }
    return root;
}

function getDepth(node) {
    if (!node) return 0;
    return 1 + Math.max(getDepth(node.left), getDepth(node.right));
}

function layoutTree(node, depth, leftBound, rightBound) {
    if (!node) return null;
    const x = (leftBound + rightBound) / 2;
    const y = depth * 65 + 30;
    const leftChild = layoutTree(node.left, depth + 1, leftBound, x);
    const rightChild = layoutTree(node.right, depth + 1, x, rightBound);
    return {
        val: node.val,
        x,
        y,
        left: leftChild,
        right: rightChild,
    };
}

function collectTreeElements(layoutNode, nodes, edges) {
    if (!layoutNode) return;
    nodes.push({ val: layoutNode.val, x: layoutNode.x, y: layoutNode.y });
    if (layoutNode.left) {
        edges.push({
            x1: layoutNode.x,
            y1: layoutNode.y,
            x2: layoutNode.left.x,
            y2: layoutNode.left.y,
        });
        collectTreeElements(layoutNode.left, nodes, edges);
    }
    if (layoutNode.right) {
        edges.push({
            x1: layoutNode.x,
            y1: layoutNode.y,
            x2: layoutNode.right.x,
            y2: layoutNode.right.y,
        });
        collectTreeElements(layoutNode.right, nodes, edges);
    }
}

/* eslint-disable react-refresh/only-export-components */
export function parseTreeInput(inputStr, defaultLabel = "") {
    const trees = [];
    const treeRegex = /(?:[a-zA-Z_]\w*\s*=\s*)?T\[(.*?)\]/g;
    let match;
    while ((match = treeRegex.exec(inputStr)) !== null) {
        const fullMatch = match[0];
        const content = match[1].trim();
        let label = defaultLabel;
        if (fullMatch.includes("=")) {
            label = fullMatch.split("=")[0].trim();
        }
        const arr = content
            ? content.split(",").map((item) => {
                  const trimmed = item.trim();
                  if (trimmed === "null" || trimmed === "None" || trimmed === "") {
                      return null;
                  }
                  const num = Number(trimmed);
                  return isNaN(num) ? trimmed : num;
              })
            : [];
        trees.push({ label, arr });
    }
    return trees;
}

export function BinaryTreeSvg({ label, arr, showRootLabel }) {
    if (!arr || arr.length === 0) return null;
    const tree = parseLevelOrder(arr);
    if (!tree) return null;
    const depth = getDepth(tree);
    const initialWidth = Math.pow(2, depth - 1) * 60 + 40;
    const layout = layoutTree(tree, 0, 20, initialWidth - 20);
    const nodes = [];
    const edges = [];
    collectTreeElements(layout, nodes, edges);
    if (nodes.length === 0) return null;
    const xs = nodes.map((n) => n.x);
    const ys = nodes.map((n) => n.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    const padding = 18;
    const width = maxX - minX + padding * 2;
    const height = maxY - minY + padding * 2;
    const shiftedNodes = nodes.map((n) => ({
        val: n.val,
        x: n.x - minX + padding,
        y: n.y - minY + padding,
    }));
    const shiftedEdges = edges.map((e) => ({
        x1: e.x1 - minX + padding,
        y1: e.y1 - minY + padding,
        x2: e.x2 - minX + padding,
        y2: e.y2 - minY + padding,
    }));
    const isOutputLabel =
        label && (label.toLowerCase() === "output" || label.toLowerCase() === "expected");
    const labelStyle = isOutputLabel ? { color: "#34D399" } : { color: "#E4E4E7" };

    return (
        <div className="flex flex-col items-center">
            {label &&
                (showRootLabel ||
                    !["root", "input", "output", "expected"].includes(label.toLowerCase())) && (
                    <div className="text-xs font-mono mb-0.5" style={labelStyle}>
                        {label}
                    </div>
                )}
            <div className="overflow-auto max-w-full">
                <svg
                    width={width}
                    height={height}
                    viewBox={`0 0 ${width} ${height}`}
                    className="overflow-visible"
                >
                    {shiftedEdges.map((e, idx) => (
                        <line
                            key={idx}
                            x1={e.x1}
                            y1={e.y1}
                            x2={e.x2}
                            y2={e.y2}
                            stroke="#3f3f46"
                            strokeWidth="2"
                        />
                    ))}
                    {shiftedNodes.map((n, idx) => (
                        <g key={idx} className="select-none">
                            <circle
                                cx={n.x}
                                cy={n.y}
                                r="16"
                                fill="#18181b"
                                stroke="#52525b"
                                strokeWidth="2"
                            />
                            <text
                                x={n.x}
                                y={n.y}
                                dy="5"
                                textAnchor="middle"
                                className="fill-zinc-100 font-mono text-md"
                            >
                                {n.val}
                            </text>
                        </g>
                    ))}
                </svg>
            </div>
        </div>
    );
}

export default function ProblemDescription({ activeProblem }) {
    const { description, examples, constraints } = activeProblem;
    const tleMs = activeProblem.timeLimit ?? 1000;
    const mleMb = activeProblem.memoryLimit ?? 128;
    const containerRef = useRef(null);

    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = 0;
        }
    }, [activeProblem.id]);

    return (
        <div
            ref={containerRef}
            className="w-full h-full bg-zinc-900/30 overflow-y-auto p-8 select-text space-y-6 desc-scrollbar"
        >
            <div className="text-zinc-100 text-[15px] leading-relaxed whitespace-pre-wrap">
                {renderMarkdown(description)}
            </div>

            {activeProblem.graphic && activeProblem.graphic !== "tree" && (
                <div className="flex justify-center bg-zinc-950/20 border border-zinc-800/40 rounded-xl p-4 overflow-hidden">
                    <img
                        src={activeProblem.graphic.replace(/^\/public/, "")}
                        alt="Problem Graphic"
                        className="max-h-[300px] object-contain rounded-lg border border-zinc-800/50"
                    />
                </div>
            )}

            {examples && examples.length > 0 && (
                <div className="space-y-5">
                    {examples.map((ex, idx) => {
                        let isClassLayout = false;
                        let parsedInput = null;
                        let parsedOutput = null;
                        if (activeProblem.code && activeProblem.code.trim().startsWith("class ")) {
                            try {
                                parsedInput = JSON.parse(depythonize(ex.input));
                                parsedOutput = JSON.parse(depythonize(ex.output));
                                if (
                                    Array.isArray(parsedInput) &&
                                    Array.isArray(parsedOutput) &&
                                    parsedInput.length === parsedOutput.length
                                ) {
                                    isClassLayout = true;
                                }
                            } catch {
                                isClassLayout = false;
                            }
                        }

                        return (
                            <div key={idx} className="space-y-2">
                                <h3 className="text-base font-semibold text-zinc-100 m-0">
                                    Example {idx + 1}:
                                </h3>
                                {(() => {
                                    if (activeProblem.graphic === null) return null;
                                    const parsedTrees = [
                                        ...parseTreeInput(ex.input, "Input"),
                                        ...parseTreeInput(ex.output, "Output"),
                                    ];
                                    const hasMultipleElementsTree = parsedTrees.some(
                                        (t) => t.arr && t.arr.length > 1,
                                    );
                                    const hasGraphicRoute =
                                        (ex.graphic && ex.graphic !== "tree") ||
                                        (activeProblem.graphic && activeProblem.graphic !== "tree");
                                    const showTree =
                                        !hasGraphicRoute &&
                                        (activeProblem.graphic === "tree" ||
                                            ex.graphic === "tree" ||
                                            hasMultipleElementsTree);
                                    if (!showTree) return null;
                                    return (
                                        <div className="flex flex-wrap gap-6 justify-center items-start py-2">
                                            {parsedTrees.map((t, idx) => (
                                                <BinaryTreeSvg
                                                    key={idx}
                                                    label={t.label}
                                                    arr={t.arr}
                                                    showRootLabel={parsedTrees.length > 1}
                                                />
                                            ))}
                                        </div>
                                    );
                                })()}
                                {(() => {
                                    if (activeProblem.graphic === null) return null;
                                    if (ex.graphic === null) return null;
                                    const parsedGrids = [
                                        ...parseGrids(ex.input, "Input"),
                                        ...parseGrids(ex.output, "Output"),
                                    ];
                                    if (parsedGrids.length === 0) return null;
                                    return (
                                        <div
                                            className="flex flex-wrap gap-6 justify-center items-start mb-1"
                                            style={{ marginTop: "2px" }}
                                        >
                                            {parsedGrids.map((g, idx) => (
                                                <GridVisualizer
                                                    key={idx}
                                                    label={parsedGrids.length > 1 ? g.label : ""}
                                                    grid={g.grid}
                                                />
                                            ))}
                                        </div>
                                    );
                                })()}
                                <div className="bg-zinc-900/40 border border-zinc-800/60 rounded-xl p-4">
                                    {isClassLayout ? (
                                        <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                            <div className="grid grid-cols-[minmax(0,1fr)_auto] gap-4 pb-1 mb-1 border-zinc-800/40 select-none">
                                                <div>
                                                    <span style={{ color: "#34D399" }}>Input</span>
                                                    <span className="text-zinc-200">:</span>
                                                </div>
                                                <div>
                                                    <span style={{ color: "#34D399" }}>Output</span>
                                                    <span className="text-zinc-200">:</span>
                                                </div>
                                            </div>
                                            {parsedInput.map((call, i) => {
                                                if (typeof call === "string") {
                                                    return (
                                                        <div
                                                            key={i}
                                                            className="grid grid-cols-[minmax(0,1fr)_auto] gap-4"
                                                        >
                                                            <div className="text-zinc-500 font-semibold">
                                                                {call}
                                                            </div>
                                                            <div className="text-zinc-500 font-semibold">
                                                                {parsedOutput &&
                                                                parsedOutput[i] !== undefined
                                                                    ? compactValue(
                                                                          pythonize(
                                                                              JSON.stringify(
                                                                                  parsedOutput[i],
                                                                              ),
                                                                          ),
                                                                      )
                                                                    : ""}
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                const [methodName, args] = call;
                                                const argsStr = args
                                                    .map((arg) =>
                                                        compactValue(
                                                            pythonize(JSON.stringify(arg)),
                                                        ),
                                                    )
                                                    .join(", ");
                                                const formattedCall = `${methodName}(${argsStr})`;
                                                const retVal = parsedOutput
                                                    ? parsedOutput[i]
                                                    : undefined;
                                                const formattedRet =
                                                    retVal !== undefined
                                                        ? compactValue(
                                                              pythonize(JSON.stringify(retVal)),
                                                          )
                                                        : "";
                                                return (
                                                    <div
                                                        key={i}
                                                        className="grid grid-cols-[minmax(0,1fr)_auto] gap-4"
                                                    >
                                                        <div className="text-zinc-200 wrap-break-word">
                                                            {highlightValue(formattedCall)}
                                                        </div>
                                                        <div className="text-zinc-200 shrink-0">
                                                            {highlightValue(formattedRet)}
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    ) : (
                                        <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                            <div className="whitespace-pre-wrap">
                                                <span
                                                    className="select-none"
                                                    style={{ color: "#34D399" }}
                                                >
                                                    Input:{" "}
                                                </span>
                                                <span className="text-zinc-200">
                                                    {highlightValue(
                                                        compactValue(pythonize(ex.input)),
                                                    )}
                                                </span>
                                            </div>
                                            <div className="whitespace-pre-wrap">
                                                <span
                                                    className="select-none"
                                                    style={{ color: "#34D399" }}
                                                >
                                                    Output:{" "}
                                                </span>
                                                <span className="text-zinc-200">
                                                    {highlightValue(
                                                        compactValue(pythonize(ex.output)),
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    )}
                                </div>
                                {ex.graphic && ex.graphic !== "tree" && (
                                    <div className="mt-3 flex justify-center bg-zinc-950/20 border border-zinc-800/40 rounded-xl p-4 overflow-hidden">
                                        <img
                                            src={ex.graphic.replace(/^\/public/, "")}
                                            alt="Example Graphic"
                                            className="max-h-[300px] object-contain rounded-lg border border-zinc-800/50"
                                        />
                                    </div>
                                )}
                                {ex.explanation && (
                                    <div className="text-zinc-300 text-[15px] leading-relaxed whitespace-pre-wrap [&_p]:inline">
                                        <span className="font-normal text-zinc-100">
                                            Explanation:{" "}
                                        </span>
                                        {renderMarkdown(ex.explanation)}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}

            {constraints && constraints.length > 0 && (
                <div className="space-y-3 pt-2">
                    <div className="flex justify-between items-center">
                        <h3 className="text-base font-semibold text-zinc-100">Constraints:</h3>
                        <div className="flex items-center gap-3 text-xs font-mono text-zinc-400 select-none">
                            <div className="flex items-center gap-1">
                                <svg
                                    className="w-3.5 h-3.5 text-zinc-500"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    strokeWidth="2.5"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <span>{tleMs} ms</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <svg
                                    className="w-3.5 h-3.5 text-zinc-500"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    strokeWidth="2.5"
                                >
                                    <ellipse cx="12" cy="5" rx="9" ry="3" />
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"
                                    />
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"
                                    />
                                </svg>
                                <span>{mleMb} MB</span>
                            </div>
                        </div>
                    </div>
                    <ul className="space-y-3 pl-4 text-zinc-100 text-[15px] leading-relaxed">
                        {constraints.map((c, idx) => (
                            <li key={idx} className="flex gap-3.5">
                                <span className="select-none shrink-0">•</span>
                                <div className="flex-1">{renderMarkdown(c)}</div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

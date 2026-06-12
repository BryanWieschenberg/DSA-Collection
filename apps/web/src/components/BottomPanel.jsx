import { useState, useEffect, useRef, useCallback } from "react";
import { driver, preloadPyodide } from "../lib/pyRunner";
import { getLimits, compactValue, pythonize, depythonize } from "../lib/appHelpers";
import SuccessAnimation from "./SuccessAnimation";
import FailureAnimation from "./FailureAnimation";
import { GridVisualizer, parseGrids } from "./GridVisualizer";
import { BinaryTreeSvg, parseTreeInput } from "./ProblemDescription";

function AutoHeightTextarea({ value, onChange, className, spellCheck }) {
    const ref = useRef(null);
    useEffect(() => {
        const adjustHeight = () => {
            if (ref.current) {
                ref.current.style.height = "auto";
                if (ref.current.scrollHeight > ref.current.clientHeight) {
                    ref.current.style.height = ref.current.scrollHeight + "px";
                }
            }
        };
        adjustHeight();
        window.addEventListener("resize", adjustHeight);
        return () => window.removeEventListener("resize", adjustHeight);
    }, [value]);
    return (
        <textarea
            ref={ref}
            value={value}
            onChange={onChange}
            className={className}
            rows={1}
            style={{ overflowY: "hidden" }}
            spellCheck={spellCheck}
        />
    );
}

const parseMethodCall = (str) => {
    str = str.trim();
    const openParen = str.indexOf("(");
    if (openParen === -1) {
        return [str, []];
    }
    const methodName = str.slice(0, openParen).trim();
    let closeParen = str.lastIndexOf(")");
    if (closeParen === -1) closeParen = str.length;
    const argsStr = str.slice(openParen + 1, closeParen).trim();
    if (!argsStr) {
        return [methodName, []];
    }
    try {
        return [methodName, JSON.parse("[" + argsStr + "]")];
    } catch {
        const args = argsStr.split(",").map((s) => {
            const trimmed = s.trim();
            if (trimmed === "true") return true;
            if (trimmed === "false") return false;
            if (trimmed === "null" || trimmed === "None") return null;
            if (!isNaN(trimmed) && trimmed !== "") return Number(trimmed);
            if (
                (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
                (trimmed.startsWith("'") && trimmed.endsWith("'"))
            ) {
                return trimmed.slice(1, -1);
            }
            return trimmed;
        });
        return [methodName, args];
    }
};

const getDefaultCases = (problem) => {
    const defaults = (problem.examples || []).map((ex) => ({
        input: compactValue(pythonize(ex.input)),
        expected: compactValue(pythonize(ex.output)),
    }));
    return defaults.length > 0 ? defaults : [{ input: "", expected: "" }];
};

export default function BottomPanel({ activeProblem, code, isSoftSolveActive }) {
    const isClass = activeProblem.code && activeProblem.code.trim().startsWith("class");
    const [activeTab, setActiveTab] = useState("testcases");
    const [testCases, setTestCases] = useState(() => getDefaultCases(activeProblem));
    const [activeCase, setActiveCase] = useState(0);
    const [localClassOps, setLocalClassOps] = useState([]);
    const [results, setResults] = useState(null);
    const [running, setRunning] = useState(false);
    const [hoveredCase, setHoveredCase] = useState(null);
    const [activeResultCase, setActiveResultCase] = useState(0);
    const [animation, setAnimation] = useState(null);
    const handleAnimationDone = useCallback(() => {
        setAnimation(null);
    }, []);

    useEffect(() => {
        preloadPyodide();
    }, []);

    useEffect(() => {
        window.dispatchEvent(new CustomEvent("dsa-running", { detail: { running } }));
    }, [running]);

    const simulateRunRef = useRef(null);
    useEffect(() => {
        simulateRunRef.current = simulateRun;
    });

    useEffect(() => {
        const handleTriggerRun = (e) => {
            simulateRunRef.current(e.detail.isSubmit);
        };
        window.addEventListener("trigger-dsa-run", handleTriggerRun);
        return () => window.removeEventListener("trigger-dsa-run", handleTriggerRun);
    }, []);

    useEffect(() => {
        const handleResetAll = () => {
            resetTestCases();
        };
        window.addEventListener("dsa-reset-all", handleResetAll);
        return () => window.removeEventListener("dsa-reset-all", handleResetAll);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        let ops = [];
        if (isClass && testCases[activeCase]) {
            try {
                const parsedInputs = JSON.parse(depythonize(testCases[activeCase].input));
                const parsedOutputs = JSON.parse(depythonize(testCases[activeCase].expected));
                if (Array.isArray(parsedInputs)) {
                    ops = parsedInputs.map((call, i) => {
                        const [methodName, args] = call;
                        const argsStr = args
                            .map((arg) => compactValue(pythonize(JSON.stringify(arg))))
                            .join(", ");
                        const formattedCall = `${methodName}(${argsStr})`;
                        const formattedRet =
                            parsedOutputs && i < parsedOutputs.length
                                ? compactValue(pythonize(JSON.stringify(parsedOutputs[i])))
                                : "None";
                        return { call: formattedCall, expected: formattedRet };
                    });
                }
            } catch {
                ops = [];
            }
        }
        const activeLocal = localClassOps.filter((op) => op.call.trim() !== "");
        const norm = (s) => (!s || s.trim() === "" || s.trim() === "None" || s.trim() === "null") ? "None" : s.trim();
        const activeLocalNorm = activeLocal.map((op) => ({ call: op.call.trim(), expected: norm(op.expected) }));
        const opsNorm = ops.map((op) => ({ call: op.call.trim(), expected: norm(op.expected) }));
        if (JSON.stringify(activeLocalNorm) !== JSON.stringify(opsNorm)) {
            if (ops.length === 0) {
                ops = [{ call: "", expected: "" }];
            }
            setLocalClassOps(ops);
        }
    }, [activeProblem, activeCase, isClass, testCases, localClassOps]);

    const resetTestCases = () => {
        const defaults = getDefaultCases(activeProblem);
        setTestCases(defaults);
        setActiveCase(0);
        setActiveResultCase(0);
        setResults(null);
        if (isClass && defaults[0]) {
            try {
                const parsedInputs = JSON.parse(depythonize(defaults[0].input));
                const parsedOutputs = JSON.parse(depythonize(defaults[0].expected));
                if (Array.isArray(parsedInputs)) {
                    const ops = parsedInputs.map((call, i) => {
                        const [methodName, args] = call;
                        const argsStr = args
                            .map((arg) => compactValue(pythonize(JSON.stringify(arg))))
                            .join(", ");
                        const formattedCall = `${methodName}(${argsStr})`;
                        const formattedRet =
                            parsedOutputs && i < parsedOutputs.length
                                ? compactValue(pythonize(JSON.stringify(parsedOutputs[i])))
                                : "None";
                        return { call: formattedCall, expected: formattedRet };
                    });
                    setLocalClassOps(ops);
                    return;
                }
            } catch {
                void 0;
            }
        }
        setLocalClassOps([{ call: "", expected: "" }]);
    };

    const updateCase = (idx, field, value) => {
        setTestCases((prev) => prev.map((tc, i) => (i === idx ? { ...tc, [field]: value } : tc)));
    };

    const addCase = () => {
        const current = testCases[activeCase] || { input: "", expected: "" };
        setTestCases((prev) => [...prev, { input: current.input, expected: current.expected }]);
        setActiveCase(testCases.length);
    };

    const deleteCase = (idx) => {
        if (testCases.length <= 1) return;
        const next = testCases.filter((_, i) => i !== idx);
        setTestCases(next);
        let targetCase = activeCase;
        if (activeCase >= next.length) targetCase = next.length - 1;
        else if (activeCase > idx) targetCase = activeCase - 1;
        setActiveCase(targetCase);

        if (isClass && next[targetCase]) {
            try {
                const parsedInputs = JSON.parse(depythonize(next[targetCase].input));
                const parsedOutputs = JSON.parse(depythonize(next[targetCase].expected));
                if (Array.isArray(parsedInputs)) {
                    const ops = parsedInputs.map((call, i) => {
                        const [methodName, args] = call;
                        const argsStr = args
                            .map((arg) => compactValue(pythonize(JSON.stringify(arg))))
                            .join(", ");
                        const formattedCall = `${methodName}(${argsStr})`;
                        const formattedRet =
                            parsedOutputs && i < parsedOutputs.length
                                ? compactValue(pythonize(JSON.stringify(parsedOutputs[i])))
                                : "None";
                        return { call: formattedCall, expected: formattedRet };
                    });
                    setLocalClassOps(ops);
                    return;
                }
            } catch {
                void 0;
            }
        }
        setLocalClassOps([{ call: "", expected: "" }]);
    };

    const simulateRun = async (isSubmit) => {
        if (running) return;
        setRunning(true);
        setActiveTab("output");
        setActiveResultCase(0);

        const isClass = activeProblem.code.trim().startsWith("class");
        const fnMatch = activeProblem.code.match(/^\s*(\w+)\s*\(/);
        const functionName = fnMatch ? fnMatch[1] : null;

        const { timeLimitMs, memLimitMb } = getLimits(activeProblem);

        const cases = testCases.map((tc) => ({
            input: tc.input,
            expected: tc.expected,
            hidden: false,
        }));

        let caseResults;
        try {
            caseResults = await driver({
                userCode: code,
                functionName,
                isClass,
                cases,
                timeLimitMs,
                memLimitMb,
                isSubmit,
                problemId: activeProblem.id,
            });
        } catch (err) {
            caseResults = testCases.map((tc, idx) => ({
                caseNum: idx + 1,
                input: tc.input,
                expected: tc.expected,
                status: "RE",
                error: String(err),
                stdout: "",
                output: null,
            }));
        }

        setResults({ isSubmit, cases: caseResults });
        const firstFailedIdx = caseResults.findIndex((c) => c.status !== "AC");
        setActiveResultCase(firstFailedIdx === -1 ? 0 : firstFailedIdx);
        if (isSubmit) {
            const allAC = caseResults.length > 0 && caseResults.every((c) => c.status === "AC");
            setAnimation(allAC ? "success" : "failure");
            if (allAC) {
                window.dispatchEvent(
                    new CustomEvent("dsa-problem-solved", {
                        detail: { id: activeProblem.id, isSoft: isSoftSolveActive },
                    }),
                );
            } else {
                window.dispatchEvent(
                    new CustomEvent("dsa-problem-wrong", {
                        detail: { id: activeProblem.id },
                    }),
                );
            }
        }
        setRunning(false);
    };

    const totalCases = results ? results.cases.length : 0;
    const passedCases = results ? results.cases.filter((c) => c.status === "AC").length : 0;
    const firstFailed = results ? results.cases.find((c) => c.status !== "AC") : null;
    const allPassed = results && passedCases === totalCases;

    const maxTimeMs = results ? Math.max(0, ...results.cases.map((c) => c.timeMs ?? 0)) : 0;
    const maxMemMb = results ? Math.max(0, ...results.cases.map((c) => c.memMb ?? 0)) : 0;

    const statusColor = (status) => {
        if (status === "AC") return "text-emerald-400";
        if (status === "WA") return "text-rose-400";
        if (status === "TLE") return "text-amber-400";
        if (status === "MLE") return "text-purple-400";
        return "text-rose-400";
    };

    const statusDot = (status) => {
        if (status === "AC") return "bg-emerald-400";
        if (status === "WA") return "bg-rose-400";
        if (status === "TLE") return "bg-amber-400";
        if (status === "MLE") return "bg-purple-400";
        return "bg-rose-400";
    };

    const statusLabel = (status) => {
        if (status === "AC") return "Correct";
        if (status === "WA") return "WRONG";
        if (status === "TLE") return "TOO SLOW";
        if (status === "MLE") return "TOO MUCH MEMORY";
        if (status === "RE") return "Error";
        return status;
    };

    const renderCaseResult = (r, hideStatus = false) => {
        const isClass = activeProblem.code && activeProblem.code.trim().startsWith("class");
        let isClassLayout = false;
        let parsedInput = null;
        let parsedOutput = null;
        let parsedExpected = null;

        if (isClass) {
            try {
                parsedInput = JSON.parse(depythonize(r.input));
                parsedExpected = JSON.parse(depythonize(r.expected));
                parsedOutput = r.output !== null ? JSON.parse(depythonize(r.output)) : null;
                if (
                    Array.isArray(parsedInput) &&
                    Array.isArray(parsedExpected) &&
                    parsedInput.length === parsedExpected.length
                ) {
                    isClassLayout = true;
                }
            } catch {
                isClassLayout = false;
            }
        }

        return (
            <div key={r.caseNum} className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                    <span className="text-zinc-300 font-semibold">
                        {r.label || `Case ${r.caseNum}`}
                    </span>
                    {!hideStatus && (
                        <span className={`font-semibold ${statusColor(r.status)}`}>
                            {statusLabel(r.status)}
                        </span>
                    )}
                    {(typeof r.timeMs === "number" || typeof r.memMb === "number") && (
                        <div className="flex items-center gap-1.5 ml-auto">
                            {typeof r.timeMs === "number" && (
                                <div className="flex items-center gap-1 px-2 py-0.5 bg-zinc-900/50 border border-zinc-800/50 rounded-md text-[11px] select-none">
                                    <span className="text-[9px] font-semibold text-zinc-500 uppercase tracking-wider">
                                        Time
                                    </span>
                                    <span className="text-zinc-100 font-mono font-medium">
                                        {r.timeMs.toFixed(3)}
                                    </span>
                                    <span className="text-zinc-400 text-[10px]">ms</span>
                                </div>
                            )}
                            {typeof r.memMb === "number" && (
                                <div className="flex items-center gap-1 px-2 py-0.5 bg-zinc-900/50 border border-zinc-800/50 rounded-md text-[11px] select-none">
                                    <span className="text-[9px] font-semibold text-zinc-500 uppercase tracking-wider">
                                        Mem
                                    </span>
                                    <span className="text-zinc-100 font-mono font-medium">
                                        {r.memMb.toFixed(3)}
                                    </span>
                                    <span className="text-zinc-400 text-[10px]">MB</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>
                {r.hidden ? (
                    <div className="space-y-3">
                        <div className="flex items-center gap-1.5 text-zinc-500 text-xs bg-zinc-800/60 rounded-lg p-2.5">
                            <svg
                                className="w-3.5 h-3.5"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <rect x="3" y="11" width="18" height="11" rx="2" />
                                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                            </svg>
                            Hidden test (input and expected output are not shown).
                        </div>
                        {r.error && r.error !== statusLabel(r.status) && (
                            <div className="bg-rose-950/30 border border-rose-900/40 rounded-lg p-3 font-mono text-xs text-rose-300">
                                {r.error}
                            </div>
                        )}
                    </div>
                ) : (
                    <>
                        {r.error && r.error !== statusLabel(r.status) && (
                            <div className="bg-rose-950/30 border border-rose-900/40 rounded-lg p-3 font-mono text-xs text-rose-300">
                                {r.error}
                            </div>
                        )}
                        {r.stdout && (
                            <div>
                                <span className="text-zinc-500 text-xs font-medium">Stdout</span>
                                <div className="bg-zinc-800/60 rounded-lg p-2 font-mono text-xs text-zinc-300 mt-1">
                                    {r.stdout}
                                </div>
                            </div>
                        )}
                        {isClassLayout ? (
                            <>
                                <div className="grid grid-cols-3 gap-4 mt-1.5">
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                            Input
                                        </span>
                                        <div className="bg-zinc-800/60 rounded-lg p-2.5 font-mono text-xs text-zinc-300 space-y-1.5">
                                            {parsedInput.map((call, i) => {
                                                const [methodName, args] = call;
                                                const argsStr = args
                                                    .map((arg) =>
                                                        compactValue(pythonize(JSON.stringify(arg))),
                                                    )
                                                    .join(", ");
                                                return (
                                                    <div
                                                        key={i}
                                                        className="truncate"
                                                        title={`${methodName}(${argsStr})`}
                                                    >{`${methodName}(${argsStr})`}</div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                            Output
                                        </span>
                                        <div
                                            className={`rounded-lg p-2.5 font-mono text-xs space-y-1.5 ${
                                                r.status === "AC"
                                                    ? "bg-emerald-950/30 border border-emerald-900/40 text-emerald-300"
                                                    : "bg-rose-950/30 border border-rose-900/40 text-rose-300"
                                            }`}
                                        >
                                            {parsedOutput
                                                ? parsedOutput.map((outVal, i) => {
                                                      const formattedOut = compactValue(
                                                          pythonize(JSON.stringify(outVal)),
                                                      );
                                                      return <div key={i}>{formattedOut}</div>;
                                                  })
                                                : "-"}
                                        </div>
                                    </div>
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                            Expected
                                        </span>
                                        <div className="bg-zinc-800/60 rounded-lg p-2.5 font-mono text-xs text-zinc-300 space-y-1.5">
                                            {parsedExpected.map((expVal, i) => {
                                                const formattedExp = compactValue(
                                                    pythonize(JSON.stringify(expVal)),
                                                );
                                                return <div key={i}>{formattedExp}</div>;
                                            })}
                                        </div>
                                    </div>
                                </div>
                                {(() => {
                                    if (activeProblem.graphic === null) return null;
                                    const outGrids = parseGrids(r.output, "Output");
                                    const outTrees = parseTreeInput(r.output, "Output");
                                    const expGrids = r.status !== "AC" ? parseGrids(r.expected, "Expected") : [];
                                    const expTrees = r.status !== "AC" ? parseTreeInput(r.expected, "Expected") : [];
                                    if (outGrids.length === 0 && outTrees.length === 0 && expGrids.length === 0 && expTrees.length === 0) {
                                        return null;
                                    }
                                    return (
                                        <div className="flex flex-wrap gap-6 justify-start items-start mt-3">
                                            {outGrids.map((g, idx) => (
                                                <GridVisualizer
                                                    key={idx}
                                                    label={outGrids.length > 1 ? g.label : "Output"}
                                                    grid={g.grid}
                                                />
                                            ))}
                                            {outTrees.map((t, idx) => (
                                                <BinaryTreeSvg
                                                    key={idx}
                                                    label={outTrees.length > 1 ? t.label : "Output"}
                                                    arr={t.arr}
                                                    showRootLabel={true}
                                                />
                                            ))}
                                            {expGrids.map((g, idx) => (
                                                <GridVisualizer
                                                    key={idx}
                                                    label={expGrids.length > 1 ? g.label : "Expected"}
                                                    grid={g.grid}
                                                />
                                            ))}
                                            {expTrees.map((t, idx) => (
                                                <BinaryTreeSvg
                                                    key={idx}
                                                    label={expTrees.length > 1 ? t.label : "Expected"}
                                                    arr={t.arr}
                                                    showRootLabel={true}
                                                />
                                            ))}
                                        </div>
                                    );
                                })()}
                            </>
                        ) : (
                            <>
                                <div>
                                    <span className="text-zinc-500 text-xs font-medium">Input</span>
                                    {(() => {
                                        if (activeProblem.graphic === null) return null;
                                        const grids = parseGrids(r.input, "Input");
                                        const trees = parseTreeInput(r.input, "Input");
                                        if (grids.length === 0 && trees.length === 0) return null;
                                        return (
                                            <div
                                                className="flex flex-wrap gap-6 justify-start items-start"
                                                style={{ marginTop: "2px" }}
                                            >
                                                {grids.map((g, idx) => (
                                                    <GridVisualizer
                                                        key={idx}
                                                        label={grids.length > 1 ? g.label : ""}
                                                        grid={g.grid}
                                                    />
                                                ))}
                                                {trees.map((t, idx) => (
                                                    <BinaryTreeSvg
                                                        key={idx}
                                                        label={t.label}
                                                        arr={t.arr}
                                                        showRootLabel={trees.length > 1}
                                                    />
                                                ))}
                                            </div>
                                        );
                                    })()}
                                    <div className="bg-zinc-800/60 rounded-lg p-2 font-mono text-xs text-zinc-300 mt-1">
                                        {r.input || "-"}
                                    </div>
                                </div>
                                {r.output !== null && (
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium">
                                            Output
                                        </span>
                                        {(() => {
                                            if (activeProblem.graphic === null) return null;
                                            const grids = parseGrids(r.output, "Output");
                                            const trees = parseTreeInput(r.output, "Output");
                                            if (grids.length === 0 && trees.length === 0)
                                                return null;
                                            return (
                                                <div
                                                    className="flex flex-wrap gap-6 justify-start items-start"
                                                    style={{ marginTop: "2px" }}
                                                >
                                                    {grids.map((g, idx) => (
                                                        <GridVisualizer
                                                            key={idx}
                                                            label={grids.length > 1 ? g.label : ""}
                                                            grid={g.grid}
                                                        />
                                                    ))}
                                                    {trees.map((t, idx) => (
                                                        <BinaryTreeSvg
                                                            key={idx}
                                                            label={t.label}
                                                            arr={t.arr}
                                                            showRootLabel={trees.length > 1}
                                                        />
                                                    ))}
                                                </div>
                                            );
                                        })()}
                                        <div
                                            className={`rounded-lg p-2 font-mono text-xs mt-1 ${
                                                r.status === "AC"
                                                    ? "bg-emerald-950/30 border border-emerald-900/40 text-emerald-300"
                                                    : "bg-rose-950/30 border border-rose-900/40 text-rose-300"
                                            }`}
                                        >
                                            {compactValue(pythonize(r.output))}
                                        </div>
                                    </div>
                                )}
                                <div>
                                    <span className="text-zinc-500 text-xs font-medium">
                                        Expected
                                    </span>
                                    {(() => {
                                        if (activeProblem.graphic === null) return null;
                                        if (r.status === "AC") return null;
                                        const grids = parseGrids(r.expected, "Expected");
                                        const trees = parseTreeInput(r.expected, "Expected");
                                        if (grids.length === 0 && trees.length === 0) return null;
                                        return (
                                            <div
                                                className="flex flex-wrap gap-6 justify-start items-start"
                                                style={{ marginTop: "2px" }}
                                            >
                                                {grids.map((g, idx) => (
                                                    <GridVisualizer
                                                        key={idx}
                                                        label={grids.length > 1 ? g.label : ""}
                                                        grid={g.grid}
                                                    />
                                                ))}
                                                {trees.map((t, idx) => (
                                                    <BinaryTreeSvg
                                                        key={idx}
                                                        label={t.label}
                                                        arr={t.arr}
                                                        showRootLabel={trees.length > 1}
                                                    />
                                                ))}
                                            </div>
                                        );
                                    })()}
                                    <div className="bg-zinc-800/60 rounded-lg p-2 font-mono text-xs text-zinc-300 mt-1">
                                        {compactValue(pythonize(r.expected)) || "-"}
                                    </div>
                                </div>
                            </>
                        )}
                        <div className="mt-4 invisible" />
                    </>
                )}
            </div>
        );
    };

    const autoRows = (text) => {
        if (!text) return 1;
        return Math.max(1, text.split("\n").length);
    };

    const handleOpChange = (index, field, value) => {
        const newOps = [...localClassOps];
        newOps[index][field] = value;
        setLocalClassOps(newOps);

        const activeOps = newOps.filter((op) => op.call.trim() !== "");
        const parsedInputs = activeOps.map((op) => {
            const [methodName, args] = parseMethodCall(op.call);
            return [methodName, args];
        });
        const parsedOutputs = activeOps.map((op) => {
            const exp = op.expected.trim();
            if (exp === "None" || exp === "null" || exp === "") return null;
            if (exp === "true") return true;
            if (exp === "false") return false;
            if (!isNaN(exp)) return Number(exp);
            try {
                return JSON.parse(exp);
            } catch {
                return exp;
            }
        });
        updateCase(activeCase, "input", JSON.stringify(parsedInputs));
        updateCase(activeCase, "expected", JSON.stringify(parsedOutputs));
    };

    const addLocalOp = () => {
        const newOps = [...localClassOps, { call: "", expected: "" }];
        setLocalClassOps(newOps);

        const activeOps = newOps.filter((op) => op.call.trim() !== "");
        const parsedInputs = activeOps.map((op) => {
            const [methodName, args] = parseMethodCall(op.call);
            return [methodName, args];
        });
        const parsedOutputs = activeOps.map((op) => {
            const exp = op.expected.trim();
            if (exp === "None" || exp === "null" || exp === "") return null;
            if (exp === "true") return true;
            if (exp === "false") return false;
            if (!isNaN(exp)) return Number(exp);
            try {
                return JSON.parse(exp);
            } catch {
                return exp;
            }
        });
        updateCase(activeCase, "input", JSON.stringify(parsedInputs));
        updateCase(activeCase, "expected", JSON.stringify(parsedOutputs));
    };

    const deleteLocalOp = (index) => {
        if (localClassOps.length <= 1) return;
        const newOps = localClassOps.filter((_, idx) => idx !== index);
        setLocalClassOps(newOps);

        const activeOps = newOps.filter((op) => op.call.trim() !== "");
        const parsedInputs = activeOps.map((op) => {
            const [methodName, args] = parseMethodCall(op.call);
            return [methodName, args];
        });
        const parsedOutputs = activeOps.map((op) => {
            const exp = op.expected.trim();
            if (exp === "None" || exp === "null" || exp === "") return null;
            if (exp === "true") return true;
            if (exp === "false") return false;
            if (!isNaN(exp)) return Number(exp);
            try {
                return JSON.parse(exp);
            } catch {
                return exp;
            }
        });
        updateCase(activeCase, "input", JSON.stringify(parsedInputs));
        updateCase(activeCase, "expected", JSON.stringify(parsedOutputs));
    };

    return (
        <div className="flex flex-col h-full bg-[#1a1a1a]">
            <div className="flex items-center justify-between px-3 pb-1.5 shrink-0 border-b border-zinc-800">
                <div className="flex items-center gap-1">
                    <button
                        onClick={() => setActiveTab("testcases")}
                        className={`px-3 py-1.5 text-xs font-medium rounded transition-colors cursor-pointer focus:outline-none ${
                            activeTab === "testcases"
                                ? "text-zinc-100 bg-zinc-700/60"
                                : "text-zinc-500 hover:text-zinc-300"
                        }`}
                    >
                        Test Cases
                    </button>
                    <button
                        onClick={() => setActiveTab("output")}
                        className={`px-3 py-1.5 text-xs font-medium rounded transition-colors cursor-pointer focus:outline-none ${
                            activeTab === "output"
                                ? "text-zinc-100 bg-zinc-700/60"
                                : "text-zinc-500 hover:text-zinc-300"
                        }`}
                    >
                        Output
                    </button>
                </div>
            </div>

            <div className="flex-1 min-h-0 overflow-y-auto p-3 desc-scrollbar">
                {activeTab === "testcases" && (
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-1.5 flex-wrap">
                                {testCases.map((_, idx) => (
                                    <div
                                        key={idx}
                                        className="relative flex"
                                        onMouseEnter={() => setHoveredCase(idx)}
                                        onMouseLeave={() => setHoveredCase(null)}
                                    >
                                        <button
                                            onClick={() => setActiveCase(idx)}
                                            className={`px-2.5 py-1 text-xs rounded transition-colors cursor-pointer focus:outline-none ${
                                                activeCase === idx
                                                    ? "bg-zinc-700 text-zinc-100"
                                                    : "bg-zinc-800/60 text-zinc-500 hover:text-zinc-300"
                                            }`}
                                        >
                                            Case {idx + 1}
                                        </button>
                                        {hoveredCase === idx && testCases.length > 1 && (
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    deleteCase(idx);
                                                }}
                                                className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-zinc-600 hover:bg-rose-500 text-zinc-300 hover:text-white rounded-full flex items-center justify-center text-[9px] leading-none transition-colors cursor-pointer focus:outline-none"
                                            >
                                                ✕
                                            </button>
                                        )}
                                    </div>
                                ))}
                                <button
                                    onClick={addCase}
                                    className="w-6 h-6 flex items-center justify-center text-sm text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors cursor-pointer focus:outline-none"
                                >
                                    +
                                </button>
                            </div>
                            <button
                                onClick={resetTestCases}
                                className="w-6 h-6 flex items-center justify-center text-zinc-500 hover:text-zinc-300 transition-colors cursor-pointer focus:outline-none"
                            >
                                <svg
                                    className="w-3.5 h-3.5"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                                    <path d="M3 3v5h5" />
                                </svg>
                            </button>
                        </div>

                        {testCases[activeCase] &&
                            (isClass ? (
                                <div>
                                    <div className="grid grid-cols-11 gap-2 text-zinc-500 text-xs font-medium mb-1 select-none">
                                        <div className="col-span-5">Input</div>
                                        <div className="col-span-5">Expected Output</div>
                                        <div className="col-span-1"></div>
                                    </div>
                                    <div className="space-y-2 pr-1">
                                        {localClassOps.map((op, i) => (
                                            <div
                                                key={i}
                                                className="grid grid-cols-11 gap-2 items-center"
                                            >
                                                <div className="col-span-5">
                                                    <input
                                                        type="text"
                                                        value={op.call}
                                                        onChange={(e) =>
                                                            handleOpChange(
                                                                i,
                                                                "call",
                                                                e.target.value,
                                                            )
                                                        }
                                                        className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg px-2.5 py-1.5 font-mono text-sm text-zinc-200 focus:outline-none focus:border-zinc-600"
                                                        spellCheck={false}
                                                    />
                                                </div>
                                                <div className="col-span-5">
                                                    <input
                                                        type="text"
                                                        value={op.expected}
                                                        onChange={(e) =>
                                                            handleOpChange(
                                                                i,
                                                                "expected",
                                                                e.target.value,
                                                            )
                                                        }
                                                        className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg px-2.5 py-1.5 font-mono text-sm text-zinc-200 focus:outline-none focus:border-zinc-600"
                                                        spellCheck={false}
                                                    />
                                                </div>
                                                <div className="col-span-1 flex justify-center">
                                                    <button
                                                        onClick={() => deleteLocalOp(i)}
                                                        disabled={localClassOps.length <= 1}
                                                        className="w-7 h-7 flex items-center justify-center rounded-lg text-zinc-500 hover:text-rose-400 hover:bg-zinc-800/50 disabled:opacity-30 disabled:hover:text-zinc-500 disabled:hover:bg-transparent transition-all cursor-pointer focus:outline-none"
                                                    >
                                                        ✕
                                                    </button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                    <button
                                        onClick={addLocalOp}
                                        className="mt-2 flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200 transition-colors cursor-pointer focus:outline-none"
                                    >
                                        + Add Operation
                                    </button>
                                    {(() => {
                                        if (activeProblem.graphic === null) return null;
                                        const expectedStr = JSON.stringify(localClassOps.map((op) => op.expected));
                                        const grids = parseGrids(expectedStr, "Expected");
                                        const trees = parseTreeInput(expectedStr, "Expected");
                                        if (grids.length === 0 && trees.length === 0) return null;
                                        return (
                                            <div className="flex flex-wrap gap-6 justify-start items-start mt-3 mb-1.5">
                                                {grids.map((g, idx) => (
                                                    <GridVisualizer
                                                        key={idx}
                                                        label={grids.length > 1 ? g.label : ""}
                                                        grid={g.grid}
                                                    />
                                                ))}
                                                {trees.map((t, idx) => (
                                                    <BinaryTreeSvg
                                                        key={idx}
                                                        label={trees.length > 1 ? t.label : ""}
                                                        arr={t.arr}
                                                        showRootLabel={true}
                                                    />
                                                ))}
                                            </div>
                                        );
                                    })()}
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                            Input
                                        </span>
                                        {(() => {
                                            if (activeProblem.graphic === null) return null;
                                            const grids = parseGrids(
                                                testCases[activeCase].input,
                                                "Input",
                                            );
                                            const trees = parseTreeInput(
                                                testCases[activeCase].input,
                                                "Input",
                                             );
                                            if (grids.length === 0 && trees.length === 0)
                                                return null;
                                            return (
                                                <div
                                                    className="flex flex-wrap gap-6 justify-start items-start mb-1.5"
                                                    style={{ marginTop: "2px" }}
                                                >
                                                    {grids.map((g, idx) => (
                                                        <GridVisualizer
                                                            key={idx}
                                                            label={grids.length > 1 ? g.label : ""}
                                                            grid={g.grid}
                                                        />
                                                    ))}
                                                    {trees.map((t, idx) => (
                                                        <BinaryTreeSvg
                                                            key={idx}
                                                            label={t.label}
                                                            arr={t.arr}
                                                            showRootLabel={trees.length > 1}
                                                        />
                                                    ))}
                                                </div>
                                            );
                                        })()}
                                        <AutoHeightTextarea
                                            value={testCases[activeCase].input}
                                            onChange={(e) =>
                                                updateCase(activeCase, "input", e.target.value)
                                            }
                                            className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg px-2.5 py-1.5 font-mono text-sm text-zinc-200 resize-none focus:outline-none focus:border-zinc-600"
                                            spellCheck={false}
                                        />
                                    </div>
                                    <div>
                                        <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                            Expected Output
                                        </span>
                                        {(() => {
                                            if (activeProblem.graphic === null) return null;
                                            const grids = parseGrids(
                                                testCases[activeCase].expected,
                                                "Expected",
                                            );
                                            const trees = parseTreeInput(
                                                testCases[activeCase].expected,
                                                "Expected",
                                            );
                                            if (grids.length === 0 && trees.length === 0)
                                                return null;
                                            return (
                                                <div
                                                    className="flex flex-wrap gap-6 justify-start items-start mb-1.5"
                                                    style={{ marginTop: "2px" }}
                                                >
                                                    {grids.map((g, idx) => (
                                                        <GridVisualizer
                                                            key={idx}
                                                            label={grids.length > 1 ? g.label : ""}
                                                            grid={g.grid}
                                                        />
                                                    ))}
                                                    {trees.map((t, idx) => (
                                                        <BinaryTreeSvg
                                                            key={idx}
                                                            label={t.label}
                                                            arr={t.arr}
                                                            showRootLabel={trees.length > 1}
                                                        />
                                                    ))}
                                                </div>
                                            );
                                        })()}
                                        <AutoHeightTextarea
                                            value={testCases[activeCase].expected}
                                            onChange={(e) =>
                                                updateCase(activeCase, "expected", e.target.value)
                                            }
                                            className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg px-2.5 py-1.5 font-mono text-sm text-zinc-200 resize-none focus:outline-none focus:border-zinc-600"
                                            spellCheck={false}
                                        />
                                    </div>
                                </div>
                            ))}
                    </div>
                )}

                {activeTab === "output" && (
                    <div>
                        {!results && !running && (
                            <div className="text-zinc-600 text-sm text-center py-6">
                                Run or submit your code to see results
                            </div>
                        )}
                        {running && (
                            <div className="text-zinc-400 text-sm text-center py-6 animate-pulse">
                                Running...
                            </div>
                        )}
                        {results && !running && (
                            <div className="space-y-4">
                                {results.isSubmit ? (
                                    <>
                                        <div className="flex items-center gap-3">
                                            <span
                                                className={`text-lg font-semibold ${allPassed ? "text-emerald-400" : statusColor(firstFailed?.status)}`}
                                            >
                                                {allPassed
                                                    ? "Accepted"
                                                    : statusLabel(firstFailed?.status)}
                                            </span>
                                            <span className="text-zinc-500 text-sm">
                                                {passedCases}/{totalCases} cases passed
                                            </span>
                                        </div>
                                        {allPassed ? (
                                            <div className="space-y-3">
                                                <div className="text-emerald-400/80 text-sm">
                                                    Your solution passed all test cases.
                                                </div>
                                                <div className="flex items-center justify-center gap-4">
                                                    <div className="w-48 flex items-center gap-3 bg-zinc-900/50 border border-zinc-800/50 rounded-xl p-3.5 hover:border-zinc-700/50 transition-all duration-200">
                                                        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-zinc-800/40 text-blue-400 shrink-0">
                                                            <svg
                                                                className="w-5 h-5"
                                                                fill="none"
                                                                viewBox="0 0 24 24"
                                                                stroke="currentColor"
                                                                strokeWidth="2"
                                                            >
                                                                <path
                                                                    strokeLinecap="round"
                                                                    strokeLinejoin="round"
                                                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                                                />
                                                            </svg>
                                                        </div>
                                                        <div>
                                                            <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">
                                                                Time
                                                            </div>
                                                            <div className="text-base font-semibold text-zinc-100 font-mono mt-0.5">
                                                                {maxTimeMs.toFixed(3)}
                                                                <span className="text-xs text-zinc-300 font-sans font-normal ml-1">
                                                                    ms
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="w-48 flex items-center gap-3 bg-zinc-900/50 border border-zinc-800/50 rounded-xl p-3.5 hover:border-zinc-700/50 transition-all duration-200">
                                                        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-zinc-800/40 text-blue-400 shrink-0">
                                                            <svg
                                                                className="w-5 h-5"
                                                                fill="none"
                                                                viewBox="0 0 24 24"
                                                                stroke="currentColor"
                                                                strokeWidth="2"
                                                            >
                                                                <ellipse
                                                                    cx="12"
                                                                    cy="5"
                                                                    rx="9"
                                                                    ry="3"
                                                                />
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
                                                        </div>
                                                        <div>
                                                            <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">
                                                                Memory
                                                            </div>
                                                            <div className="text-base font-semibold text-zinc-100 font-mono mt-0.5">
                                                                {maxMemMb.toFixed(3)}
                                                                <span className="text-xs text-zinc-300 font-sans font-normal ml-1">
                                                                    MB
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ) : (
                                            firstFailed && renderCaseResult(firstFailed, true)
                                        )}
                                    </>
                                ) : (
                                    <div className="space-y-3">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-1.5 flex-wrap">
                                                {results.cases.map((r, idx) => (
                                                    <button
                                                        key={idx}
                                                        onClick={() => setActiveResultCase(idx)}
                                                        className={`px-2.5 py-1 text-xs rounded transition-colors cursor-pointer focus:outline-none ${
                                                            activeResultCase === idx
                                                                ? "bg-zinc-700 text-zinc-100"
                                                                : "bg-zinc-800/60 text-zinc-500 hover:text-zinc-300"
                                                        }`}
                                                    >
                                                        <span
                                                            className={`inline-block align-middle w-1.5 h-1.5 rounded-full mr-1.5 ${statusDot(r.status)}`}
                                                        />
                                                        {r.label || `Case ${r.caseNum}`}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                        {results.cases[activeResultCase] &&
                                            renderCaseResult(results.cases[activeResultCase])}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {animation === "success" && <SuccessAnimation onDone={handleAnimationDone} />}
            {animation === "failure" && <FailureAnimation onDone={handleAnimationDone} />}
        </div>
    );
}

import { useState, useEffect, useRef } from "react";
import { driver, preloadPyodide } from "../lib/pyRunner";
import { getLimits, getHiddenTests } from "../lib/appHelpers";

const getDefaultCases = (problem) => {
    const defaults = (problem.examples || []).map((ex) => ({
        input: ex.input,
        expected: ex.output,
    }));
    return defaults.length > 0 ? defaults : [{ input: "", expected: "" }];
};

export default function BottomPanel({ activeProblem, code }) {
    const [activeTab, setActiveTab] = useState("testcases");
    const [testCases, setTestCases] = useState(() => getDefaultCases(activeProblem));
    const [activeCase, setActiveCase] = useState(0);
    const [results, setResults] = useState(null);
    const [running, setRunning] = useState(false);
    const [hoveredCase, setHoveredCase] = useState(null);
    const [activeResultCase, setActiveResultCase] = useState(0);

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
    }, []);

    const resetTestCases = () => {
        setTestCases(getDefaultCases(activeProblem));
        setActiveCase(0);
        setActiveResultCase(0);
        setResults(null);
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
        if (activeCase >= next.length) setActiveCase(next.length - 1);
        else if (activeCase > idx) setActiveCase(activeCase - 1);
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
        if (isSubmit) {
            for (const ht of getHiddenTests(activeProblem)) {
                cases.push({ input: ht.input, expected: ht.expected ?? ht.output, hidden: true });
            }
        }

        let caseResults;
        try {
            caseResults = await driver({
                userCode: code,
                functionName,
                isClass,
                cases,
                timeLimitMs,
                memLimitMb,
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
            if (allAC) {
                window.dispatchEvent(
                    new CustomEvent("dsa-problem-solved", {
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
        if (status === "AC") return "Accepted";
        if (status === "WA") return "Wrong Answer";
        if (status === "TLE") return "Time Limit Exceeded";
        if (status === "MLE") return "Memory Limit Exceeded";
        if (status === "RE") return "Runtime Error";
        return status;
    };

    const renderCaseResult = (r) => (
        <div key={r.caseNum} className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
                <span className="text-zinc-500 font-medium">
                    {r.label || `Case ${r.caseNum}`}:
                </span>
                <span className={`font-semibold ${statusColor(r.status)}`}>
                    {statusLabel(r.status)}
                </span>
                {(typeof r.timeMs === "number" || typeof r.memMb === "number") && (
                    <span className="text-zinc-500 text-xs ml-auto font-mono">
                        {typeof r.timeMs === "number" && `${r.timeMs.toFixed(1)} ms`}
                        {typeof r.timeMs === "number" && typeof r.memMb === "number" && " · "}
                        {typeof r.memMb === "number" && `${r.memMb.toFixed(2)} MB`}
                    </span>
                )}
            </div>
            {r.hidden ? (
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
                    Hidden test — input and expected output are not shown.
                </div>
            ) : (
                <>
            {r.error && (
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
            <div className="grid grid-cols-2 gap-3">
                <div>
                    <span className="text-zinc-500 text-xs font-medium">Input</span>
                    <div className="bg-zinc-800/60 rounded-lg p-2 font-mono text-xs text-zinc-300 mt-1">
                        {r.input || "—"}
                    </div>
                </div>
                <div>
                    <span className="text-zinc-500 text-xs font-medium">Expected</span>
                    <div className="bg-zinc-800/60 rounded-lg p-2 font-mono text-xs text-zinc-300 mt-1">
                        {r.expected || "—"}
                    </div>
                </div>
            </div>
            {r.output !== null && (
                <div>
                    <span className="text-zinc-500 text-xs font-medium">Output</span>
                    <div
                        className={`rounded-lg p-2 font-mono text-xs mt-1 ${
                            r.status === "AC"
                                ? "bg-emerald-950/30 border border-emerald-900/40 text-emerald-300"
                                : "bg-rose-950/30 border border-rose-900/40 text-rose-300"
                        }`}
                    >
                        {r.output}
                    </div>
                </div>
            )}
                </>
            )}
        </div>
    );

    const autoRows = (text) => {
        if (!text) return 1;
        return Math.max(1, text.split("\n").length);
    };

    return (
        <div className="flex flex-col h-full bg-[#1e1e1e]">
            <div className="flex items-center justify-between px-3 py-1.5 shrink-0">
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

            <div className="flex-1 min-h-0 overflow-y-auto p-3 panel-scrollbar">
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

                        {testCases[activeCase] && (
                            <div className="space-y-3">
                                <div>
                                    <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                        Input
                                    </span>
                                    <textarea
                                        value={testCases[activeCase].input}
                                        onChange={(e) =>
                                            updateCase(activeCase, "input", e.target.value)
                                        }
                                        className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg p-2.5 font-mono text-sm text-zinc-200 resize-none focus:outline-none focus:border-zinc-600"
                                        rows={autoRows(testCases[activeCase].input)}
                                        spellCheck={false}
                                    />
                                </div>
                                <div>
                                    <span className="text-zinc-500 text-xs font-medium mb-1 block">
                                        Expected Output
                                    </span>
                                    <textarea
                                        value={testCases[activeCase].expected}
                                        onChange={(e) =>
                                            updateCase(activeCase, "expected", e.target.value)
                                        }
                                        className="w-full bg-zinc-800/60 border border-zinc-700/40 rounded-lg p-2.5 font-mono text-sm text-zinc-200 resize-none focus:outline-none focus:border-zinc-600"
                                        rows={autoRows(testCases[activeCase].expected)}
                                        spellCheck={false}
                                    />
                                </div>
                            </div>
                        )}
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
                                                <div className="flex items-center gap-3">
                                                    <div className="flex-1 bg-zinc-800/60 rounded-lg p-3">
                                                        <div className="text-zinc-500 text-xs font-medium">
                                                            Time
                                                        </div>
                                                        <div className="text-zinc-100 font-mono text-sm mt-0.5">
                                                            {maxTimeMs.toFixed(1)} ms
                                                        </div>
                                                    </div>
                                                    <div className="flex-1 bg-zinc-800/60 rounded-lg p-3">
                                                        <div className="text-zinc-500 text-xs font-medium">
                                                            Memory
                                                        </div>
                                                        <div className="text-zinc-100 font-mono text-sm mt-0.5">
                                                            {maxMemMb.toFixed(2)} MB
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ) : (
                                            firstFailed && renderCaseResult(firstFailed)
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
        </div>
    );
}

import { useState, useEffect, useRef } from "react";

export default function Sidebar({
    sidebarOpen,
    onClose,
    allProblems,
    completedProblems,
    softSolvedProblems = new Set(),
    activeProblem,
    onSelectProblem,
    onToggleCompleted,
    onResetAll,
    onResetSoftCodes,
    onResetProblemCode,
}) {
    const easyCount = allProblems.filter((p) => p.difficulty === "Easy").length;
    const mediumCount = allProblems.filter((p) => p.difficulty === "Medium").length;
    const hardCount = allProblems.filter((p) => p.difficulty === "Hard").length;
    const extremeCount = allProblems.filter((p) => p.difficulty === "Extreme").length;

    const easySolved = allProblems.filter(
        (p) => p.difficulty === "Easy" && completedProblems.has(p.id),
    ).length;
    const mediumSolved = allProblems.filter(
        (p) => p.difficulty === "Medium" && completedProblems.has(p.id),
    ).length;
    const hardSolved = allProblems.filter(
        (p) => p.difficulty === "Hard" && completedProblems.has(p.id),
    ).length;
    const extremeSolved = allProblems.filter(
        (p) => p.difficulty === "Extreme" && completedProblems.has(p.id),
    ).length;

    const [confirmReset, setConfirmReset] = useState(false);
    const activeItemRef = useRef(null);
    const containerRef = useRef(null);

    useEffect(() => {
        if (sidebarOpen && activeItemRef.current && containerRef.current) {
            const timer = setTimeout(() => {
                const container = containerRef.current;
                const element = activeItemRef.current;
                const targetScrollTop = element.offsetTop - container.clientHeight * 0.3;
                container.scrollTo({
                    top: targetScrollTop,
                    behavior: "auto",
                });
            }, 50);
            return () => clearTimeout(timer);
        }
    }, [sidebarOpen]);
    const [confirmResetSoft, setConfirmResetSoft] = useState(false);

    if (!sidebarOpen && (confirmReset || confirmResetSoft)) {
        setConfirmReset(false);
        setConfirmResetSoft(false);
    }

    const handleResetAllClick = () => {
        if (confirmReset) {
            onResetAll();
            setConfirmReset(false);
        } else {
            setConfirmReset(true);
            setTimeout(() => {
                setConfirmReset(false);
            }, 1000);
        }
    };

    const handleResetSoftClick = (e) => {
        e.stopPropagation();
        if (confirmResetSoft) {
            onResetSoftCodes();
            setConfirmResetSoft(false);
        } else {
            setConfirmResetSoft(true);
            setTimeout(() => {
                setConfirmResetSoft(false);
            }, 1000);
        }
    };

    return (
        <>
            {sidebarOpen && (
                <div
                    onClick={onClose}
                    className="fixed inset-0 bg-zinc-950/60 backdrop-blur-[2px] z-30 transition-opacity"
                />
            )}

            <aside
                className={`fixed inset-y-0 right-0 w-[600px] bg-zinc-900 border-l border-zinc-800 z-40 transform transition-transform duration-300 ease-in-out flex flex-col ${
                    sidebarOpen ? "translate-x-0" : "translate-x-full"
                }`}
            >
                <div className="p-4 border-b border-zinc-800 flex items-center justify-between shrink-0">
                    <h2 className="font-semibold text-zinc-200">Select Problem</h2>
                    <div className="flex items-center gap-2">
                        <div className="relative flex items-center">
                            {confirmResetSoft && (
                                <span className="absolute right-full mr-2 text-[10px] text-amber-500 font-semibold whitespace-nowrap bg-zinc-950 border border-amber-600 px-1.5 py-0.5 rounded">
                                    Click again to confirm
                                </span>
                            )}
                            <button
                                onClick={handleResetSoftClick}
                                className={`p-1.5 rounded transition-colors cursor-pointer focus:outline-none ${
                                    confirmResetSoft
                                        ? "bg-amber-500 text-zinc-950 hover:bg-amber-400"
                                        : "text-amber-500 hover:text-amber-400 hover:bg-zinc-800"
                                }`}
                            >
                                <svg
                                    className="w-4 h-4"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2.5"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                                    <path d="M3 3v5h5" />
                                </svg>
                            </button>
                        </div>

                        <div className="relative flex items-center">
                            {confirmReset && (
                                <span className="absolute right-full mr-2 text-[10px] text-rose-500 font-semibold whitespace-nowrap bg-zinc-950 border border-rose-600 px-1.5 py-0.5 rounded">
                                    Click again to confirm
                                </span>
                            )}
                            <button
                                onClick={handleResetAllClick}
                                className={`p-1.5 rounded transition-colors cursor-pointer focus:outline-none ${
                                    confirmReset
                                        ? "bg-rose-600 text-white hover:bg-rose-500"
                                        : "text-rose-500 hover:text-rose-400 hover:bg-zinc-800"
                                }`}
                            >
                                <svg
                                    className="w-4 h-4"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2.5"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M3 6h18" />
                                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                                </svg>
                            </button>
                        </div>

                        <div className="w-px h-4 bg-zinc-800 mx-0.5" />

                        <button
                            onClick={onClose}
                            className="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors cursor-pointer focus:outline-none"
                        >
                            <svg
                                className="w-4 h-4"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2.5}
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                        </button>
                    </div>
                </div>

                <div className="px-4 py-2.5 bg-zinc-950/40 border-b border-zinc-800 flex items-center justify-center gap-3 text-[11px] font-medium shrink-0 select-none">
                    {easyCount >= 1 && (
                        <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            Easy:{" "}
                            <span className="font-semibold text-zinc-200">
                                {easySolved}/{easyCount}
                            </span>
                        </span>
                    )}
                    {mediumCount >= 1 && (
                        <span className="px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
                            Medium:{" "}
                            <span className="font-semibold text-zinc-200">
                                {mediumSolved}/{mediumCount}
                            </span>
                        </span>
                    )}
                    {hardCount >= 1 && (
                        <span className="px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
                            Hard:{" "}
                            <span className="font-semibold text-zinc-200">
                                {hardSolved}/{hardCount}
                            </span>
                        </span>
                    )}
                    {extremeCount >= 1 && (
                        <span className="px-2.5 py-0.5 rounded-full bg-purple-500/15 text-purple-400 border border-purple-500/30">
                            Extreme:{" "}
                            <span className="font-semibold text-zinc-200">
                                {extremeSolved}/{extremeCount}
                            </span>
                        </span>
                    )}
                </div>

                <div ref={containerRef} className="flex-1 overflow-y-auto p-4 space-y-1">
                    {allProblems.map((prob, index) => {
                        const isSolved = completedProblems.has(prob.id);
                        const isSoftSolved = softSolvedProblems.has(prob.id) && !isSolved;
                        const diff = prob.difficulty;
                        const isActive = activeProblem.id === prob.id;

                        return (
                            <div
                                key={prob.id}
                                ref={isActive ? activeItemRef : null}
                                onClick={() => onSelectProblem(prob)}
                                className={`group px-3 h-9 flex items-center justify-between text-xs transition-colors cursor-pointer rounded-lg ${
                                    isActive ? "bg-zinc-800/90" : "hover:bg-zinc-800/70"
                                }`}
                            >
                                <div className="flex items-center gap-2.5 min-w-0 pr-2">
                                    <div
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onToggleCompleted(prob.id, e);
                                        }}
                                        className={`w-4 h-4 cursor-pointer rounded flex items-center justify-center border transition-colors shrink-0 ${
                                            isSolved
                                                ? "bg-emerald-500 border-emerald-400 text-zinc-950"
                                                : isSoftSolved
                                                  ? "bg-zinc-500 border-zinc-400 text-zinc-950"
                                                  : "border-zinc-700 bg-zinc-950"
                                        }`}
                                    >
                                        {(isSolved || isSoftSolved) && (
                                            <svg
                                                className="w-2.5 h-2.5 stroke-2"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    d="M5 13l4 4L19 7"
                                                />
                                            </svg>
                                        )}
                                    </div>
                                    <span
                                        className={`truncate transition-colors ${isActive ? "text-zinc-100 font-medium" : "text-zinc-400 group-hover:text-zinc-200"}`}
                                    >
                                        {index + 1}. {prob.name}
                                    </span>
                                </div>
                                <div className="flex items-center gap-2 shrink-0">
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onResetProblemCode(prob.id);
                                        }}
                                        className="hidden group-hover:flex items-center justify-center h-5 w-5 text-zinc-500 hover:text-rose-400 cursor-pointer focus:outline-none"
                                    >
                                        <svg
                                            className="w-3.5 h-3.5"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            strokeWidth="2.5"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                        >
                                            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                                            <path d="M3 3v5h5" />
                                        </svg>
                                    </button>
                                    <span
                                        className={`text-[9px] font-medium px-1 py-0.2 rounded ${
                                            diff === "Easy"
                                                ? "text-emerald-400"
                                                : diff === "Medium"
                                                  ? "text-amber-400"
                                                  : diff === "Hard"
                                                    ? "text-rose-400"
                                                    : "text-purple-400 font-bold"
                                        }`}
                                    >
                                        {diff}
                                    </span>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </aside>
        </>
    );
}

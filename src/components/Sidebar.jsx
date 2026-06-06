import { useState, useEffect } from "react";

export default function Sidebar({
    sidebarOpen,
    onClose,
    allProblems,
    completedProblems,
    activeProblem,
    onSelectProblem,
    onToggleCompleted,
    onResetAll,
}) {
    const [confirmReset, setConfirmReset] = useState(false);

    useEffect(() => {
        if (!sidebarOpen) {
            setConfirmReset(false);
        }
    }, [sidebarOpen]);

    const handleResetAllClick = () => {
        if (confirmReset) {
            onResetAll();
            setConfirmReset(false);
        } else {
            setConfirmReset(true);
            setTimeout(() => {
                setConfirmReset(false);
            }, 3000);
        }
    };

    return (
        <>
            {sidebarOpen && (
                <div
                    onClick={onClose}
                    className="fixed inset-0 bg-zinc-950/60 backdrop-blur-xs z-30 transition-opacity"
                />
            )}

            <aside
                className={`fixed inset-y-0 right-0 w-80 bg-zinc-900 border-l border-zinc-800 z-40 transform transition-transform duration-300 ease-in-out flex flex-col ${
                    sidebarOpen ? "translate-x-0" : "translate-x-full"
                }`}
            >
                <div className="p-4 border-b border-zinc-800 flex items-center justify-between shrink-0">
                    <h2 className="font-semibold text-zinc-200">Select Problem</h2>
                    <button
                        onClick={onClose}
                        className="text-zinc-400 hover:text-zinc-200 transition-colors cursor-pointer focus:outline-none"
                    >
                        <svg
                            className="w-5 h-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-1">
                    {allProblems.map((prob, index) => {
                        const isSolved = completedProblems.has(prob.id);
                        const diff = prob.difficulty;
                        const isActive = activeProblem.id === prob.id;

                        return (
                            <div
                                key={prob.id}
                                onClick={() => onSelectProblem(prob)}
                                className={`px-3 py-2 flex items-center justify-between text-xs transition-colors cursor-pointer rounded-lg ${
                                    isActive ? "bg-zinc-800/80" : "hover:bg-zinc-800/40"
                                }`}
                            >
                                <div className="flex items-center gap-2.5 min-w-0 pr-2">
                                    <button
                                        onClick={(e) => onToggleCompleted(prob.id, e)}
                                        className={`w-4 h-4 rounded flex items-center justify-center border transition-colors cursor-pointer focus:outline-none shrink-0 ${
                                            isSolved
                                                ? "bg-emerald-500 border-emerald-400 text-zinc-950"
                                                : "border-zinc-700 hover:border-zinc-500 bg-zinc-950"
                                        }`}
                                    >
                                        {isSolved && (
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
                                    </button>
                                    <span
                                        className={`truncate ${isActive ? "text-zinc-100 font-medium" : "text-zinc-400"}`}
                                    >
                                        {index + 1}. {prob.name}
                                    </span>
                                </div>
                                <span
                                    className={`text-[9px] font-medium shrink-0 px-1 py-0.2 rounded ${
                                        diff === "Easy"
                                            ? "text-emerald-400"
                                            : diff === "Medium"
                                              ? "text-amber-400"
                                              : "text-rose-400"
                                    }`}
                                >
                                    {diff}
                                </span>
                            </div>
                        );
                    })}
                </div>

                <div className="p-4 border-t border-zinc-800 shrink-0">
                    <button
                        onClick={handleResetAllClick}
                        className={`w-full py-2 px-3 text-xs font-semibold rounded-lg transition-colors cursor-pointer focus:outline-none ${
                            confirmReset
                                ? "bg-rose-600 hover:bg-rose-500 text-white"
                                : "bg-zinc-800 hover:bg-zinc-700 text-zinc-300"
                        }`}
                    >
                        {confirmReset ? "Click again to confirm reset" : "Reset All Progress"}
                    </button>
                </div>
            </aside>
        </>
    );
}

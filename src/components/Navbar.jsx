import { useState, useEffect } from "react";

export default function Navbar({
    onOpenSidebar,
    activeProblem,
    allProblems,
    completedCount,
    totalCount,
    onResetCode,
    onSelectProblem,
}) {
    const activeIndex = allProblems.findIndex((p) => p.id === activeProblem.id);
    const problemNumber = activeIndex !== -1 ? activeIndex + 1 : 1;
    const prevProblem = activeIndex > 0 ? allProblems[activeIndex - 1] : null;
    const nextProblem = activeIndex < allProblems.length - 1 ? allProblems[activeIndex + 1] : null;

    const [time, setTime] = useState(0);
    const [timerRunning, setTimerRunning] = useState(true);

    useEffect(() => {
        let interval = null;
        if (timerRunning) {
            interval = setInterval(() => {
                setTime((prev) => prev + 1);
            }, 1000);
        } else {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [timerRunning]);

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    };

    const [lives, setLives] = useState(3);

    return (
        <header className="h-14 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between px-6 z-20 shrink-0">
            <div className="flex items-center gap-2.5">
                <span className="font-semibold text-zinc-200 text-xl">
                    {problemNumber}. {activeProblem.name}
                </span>
                <span
                    className={`text-sm ml-4 px-1.5 py-0.5 rounded font-medium ${
                        activeProblem.difficulty === "Easy"
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                            : activeProblem.difficulty === "Medium"
                              ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                              : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                    }`}
                >
                    {activeProblem.difficulty}
                </span>
            </div>

            <div className="flex items-center gap-4">
                <div className="flex items-center gap-1">
                    <button
                        onClick={() => prevProblem && onSelectProblem(prevProblem)}
                        disabled={!prevProblem}
                        className="p-1.5 text-zinc-400 hover:text-zinc-200 disabled:opacity-25 disabled:hover:text-zinc-400 transition-colors cursor-pointer disabled:cursor-not-allowed focus:outline-none"
                        title="Previous problem"
                    >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                        </svg>
                    </button>
                    <button
                        onClick={() => nextProblem && onSelectProblem(nextProblem)}
                        disabled={!nextProblem}
                        className="p-1.5 text-zinc-400 hover:text-zinc-200 disabled:opacity-25 disabled:hover:text-zinc-400 transition-colors cursor-pointer disabled:cursor-not-allowed focus:outline-none"
                        title="Next problem"
                    >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                        </svg>
                    </button>
                </div>

                <div className="text-xs text-zinc-400 font-medium">
                    Solved: <span className="text-emerald-400">{completedCount}</span> /{" "}
                    {totalCount}
                </div>

                <button
                    onClick={() => setTimerRunning(!timerRunning)}
                    className="flex items-center gap-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-3 py-1.5 rounded-lg text-xs transition-colors border border-zinc-700/50 cursor-pointer focus:outline-none"
                    title={timerRunning ? "Pause Timer" : "Start Timer"}
                >
                    <svg
                        className={`w-3.5 h-3.5 ${timerRunning ? "text-emerald-400 animate-pulse" : "text-zinc-400"}`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={2}
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                        />
                    </svg>
                    <span className="font-mono">{formatTime(time)}</span>
                </button>

                <button
                    onClick={() => setLives((prev) => (prev > 1 ? prev - 1 : 3))}
                    className="flex items-center gap-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-3 py-1.5 rounded-lg text-xs transition-colors border border-zinc-700/50 cursor-pointer focus:outline-none"
                    title="Click to decrement lives (resets at 0)"
                >
                    <span className="text-rose-500">
                        {"❤️".repeat(lives) + "🖤".repeat(3 - lives)}
                    </span>
                </button>

                <button
                    onClick={onResetCode}
                    className="flex items-center justify-center bg-zinc-800 hover:bg-zinc-700 hover:text-rose-400 text-zinc-300 p-2 rounded-lg transition-colors border border-zinc-700/50 cursor-pointer focus:outline-none"
                    title="Reset to default template"
                >
                    <svg
                        className="w-4 h-4"
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

                <button
                    onClick={onOpenSidebar}
                    className="flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-3.5 py-1.5 rounded-lg text-sm transition-colors border border-zinc-700/50 cursor-pointer focus:outline-none"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4 6h16M4 12h16M4 18h16"
                        />
                    </svg>
                    <span>Problems</span>
                </button>
            </div>
        </header>
    );
}

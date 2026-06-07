export default function Navbar({
    onOpenSidebar,
    activeProblem,
    allProblems,
    completedCount,
    totalCount,
    onResetCode,
    onSelectProblem,
    time,
    timerRunning,
    setTimerRunning,
    lives,
    isSoftSolveActive,
    dailyScore = 0,
}) {
    const activeIndex = allProblems.findIndex((p) => p.id === activeProblem.id);
    const problemNumber = activeIndex !== -1 ? activeIndex + 1 : 1;
    const prevProblem = activeIndex > 0 ? allProblems[activeIndex - 1] : null;
    const nextProblem = activeIndex < allProblems.length - 1 ? allProblems[activeIndex + 1] : null;

    const formatTime = (seconds) => {
        const isNegative = seconds < 0;
        const absSeconds = Math.abs(seconds);
        const mins = Math.floor(absSeconds / 60);
        const secs = absSeconds % 60;
        const formatted = `${mins}:${secs.toString().padStart(2, "0")}`;
        return isNegative ? `-${formatted}` : formatted;
    };

    const renderHearts = () => {
        const hearts = [];
        for (let i = 0; i < 3; i++) {
            const isFilled = i < lives;
            hearts.push(
                <svg
                    key={i}
                    className={`w-5 h-5 transition-all duration-300 ${
                        isFilled
                            ? "text-rose-500 fill-rose-500"
                            : "text-zinc-600 fill-zinc-700 opacity-40"
                    }`}
                    viewBox="0 0 24 24"
                >
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>,
            );
        }
        return hearts;
    };

    return (
        <header className="h-14 bg-zinc-900 border-b border-zinc-800 grid grid-cols-3 items-center px-6 z-20 shrink-0">
            <div className="flex items-center gap-2.5 justify-self-start">
                <div className="flex items-center gap-1 mr-1">
                    <button
                        onClick={() => prevProblem && onSelectProblem(prevProblem)}
                        disabled={!prevProblem}
                        className="p-1.5 text-zinc-400 hover:text-zinc-200 disabled:opacity-25 disabled:hover:text-zinc-400 transition-colors cursor-pointer disabled:cursor-not-allowed focus:outline-none"
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
                                d="M15.75 19.5 8.25 12l7.5-7.5"
                            />
                        </svg>
                    </button>
                    <button
                        onClick={() => nextProblem && onSelectProblem(nextProblem)}
                        disabled={!nextProblem}
                        className="p-1.5 text-zinc-400 hover:text-zinc-200 disabled:opacity-25 disabled:hover:text-zinc-400 transition-colors cursor-pointer disabled:cursor-not-allowed focus:outline-none"
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
                                d="m8.25 4.5 7.5 7.5-7.5 7.5"
                            />
                        </svg>
                    </button>
                </div>

                <span className="font-semibold text-zinc-200 text-xl">
                    {problemNumber}. {activeProblem.name}
                </span>

                <span
                    className={`text-sm ml-1.5 px-1.5 py-0.5 rounded font-medium ${
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

            <div className="flex items-center justify-center justify-self-center">
                <div className="w-28 flex items-center justify-end">
                    <div className="flex items-center gap-2 text-zinc-200 text-lg">
                        <svg
                            className={`w-5 h-5 ${timerRunning ? "text-emerald-400" : "text-zinc-400"}`}
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
                        <span className={`font-mono ${time < 0 ? "text-rose-500" : ""}`}>
                            {formatTime(time)}
                        </span>
                    </div>
                </div>

                <div
                    className={`${isSoftSolveActive ? "w-16" : "w-6"} flex items-center justify-center transition-all duration-300`}
                >
                    {isSoftSolveActive && (
                        <div className="text-amber-500 flex items-center justify-center">
                            <svg
                                className="w-6 h-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2.5}
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3Z"
                                />
                            </svg>
                        </div>
                    )}
                </div>

                <div className="w-28 flex items-center justify-start">
                    <div className="flex items-center gap-1">{renderHearts()}</div>
                </div>
            </div>

            <div className="flex items-center gap-5 justify-self-end">
                <div className="flex items-center gap-1.5 text-zinc-200 text-sm">
                    <span className="text-zinc-400 font-medium">Today:</span>
                    <span
                        className={`font-semibold transition-all duration-300 ${
                            dailyScore >= 200
                                ? "text-amber-400 drop-shadow-[0_0_8px_rgba(245,158,11,0.6)] font-bold animate-pulse"
                                : "text-zinc-200"
                        }`}
                    >
                        {dailyScore}
                    </span>
                </div>

                <div className="text-sm text-zinc-400 font-medium">
                    Solved: <span className="text-emerald-400 font-semibold">{completedCount}</span>{" "}
                    <span className="text-zinc-200">/ {totalCount}</span>
                </div>

                <button
                    onClick={onResetCode}
                    className="flex items-center justify-center hover:text-white text-zinc-400 p-1.5 transition-colors cursor-pointer focus:outline-none"
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

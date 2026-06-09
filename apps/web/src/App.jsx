import { useState, useEffect, useRef, useMemo } from "react";
import Editor from "./components/Editor";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import ProblemDescription from "./components/ProblemDescription";
import BottomPanel from "./components/BottomPanel";
import {
    getTemplateCode,
    slugify,
    findProblemById,
    allProblems,
    getTodayNY,
} from "./lib/appHelpers";

const createPrng = (seed) => {
    let s = seed;
    return () => {
        s = (s * 1664525 + 1013904223) % 4294967296;
        return s / 4294967296;
    };
};

export default function App() {
    const [activeProblem, setActiveProblem] = useState(() => {
        const slug = window.location.pathname.replace(/^\//, "");
        if (slug) {
            const prob = allProblems.find((p) => slugify(p.name) === slug);
            if (prob) return prob;
        }
        const savedId = localStorage.getItem("dsa-active-problem-id");
        if (savedId) {
            const prob = findProblemById(parseInt(savedId, 10));
            if (prob) return prob;
        }
        return allProblems[0];
    });

    const embers = useMemo(() => {
        if (activeProblem.difficulty !== "Extreme") return [];
        const rand = createPrng(activeProblem.id);
        return Array.from({ length: 50 }, (_, i) => {
            const startFromBottom = rand() > 0.4;
            let left, bottom, tx, ty;
            if (startFromBottom) {
                left = `${rand() * 80 + 30}%`;
                bottom = `-40px`;
                tx = `-${rand() * 60 + 30}vw`;
                ty = `-${rand() * 30 + 90}vh`;
            } else {
                left = `105%`;
                bottom = `${rand() * 80 - 10}vh`;
                tx = `-${rand() * 60 + 60}vw`;
                ty = `-${rand() * 30 + 50}vh`;
            }
            return {
                id: i,
                left,
                bottom,
                size: `${rand() * 5 + 3}px`,
                duration: `${rand() * 5 + 4}s`,
                delay: `${rand() * 8}s`,
                tx,
                ty,
                rot: `${rand() * 360 + 180}deg`,
            };
        });
    }, [activeProblem.id, activeProblem.difficulty]);

    const [code, setCode] = useState(() => {
        const savedCode = localStorage.getItem(`dsa-code-${activeProblem.id}`);
        if (savedCode !== null) return savedCode;
        return getTemplateCode(activeProblem);
    });

    const [completedProblems, setCompletedProblems] = useState(() => {
        const saved = localStorage.getItem("dsa-completed-problems");
        return saved ? new Set(JSON.parse(saved)) : new Set();
    });

    const [softSolvedProblems, setSoftSolvedProblems] = useState(() => {
        const saved = localStorage.getItem("dsa-soft-solved-problems");
        return saved ? new Set(JSON.parse(saved)) : new Set();
    });

    const [solveHistory, setSolveHistory] = useState(() => {
        const saved = localStorage.getItem("dsa-solve-history");
        return saved ? JSON.parse(saved) : [];
    });

    const getInitialTime = (difficulty) => {
        if (difficulty === "Easy") return 300;
        if (difficulty === "Medium") return 1200;
        if (difficulty === "Hard") return 2400;
        if (difficulty === "Extreme") return 3600;
        return 300;
    };

    const [time, setTime] = useState(() => getInitialTime(activeProblem.difficulty));
    const [timerRunning, setTimerRunning] = useState(
        () => !completedProblems.has(activeProblem.id),
    );
    const [lives, setLives] = useState(3);
    const [tabSwitched, setTabSwitched] = useState(false);

    const [prevProblemId, setPrevProblemId] = useState(activeProblem.id);
    if (activeProblem.id !== prevProblemId) {
        setPrevProblemId(activeProblem.id);
        setTime(getInitialTime(activeProblem.difficulty));
        setLives(3);
        setTabSwitched(false);
        setTimerRunning(!completedProblems.has(activeProblem.id));
    }

    useEffect(() => {
        let interval = null;
        if (timerRunning) {
            interval = setInterval(() => {
                setTime((prev) => prev - 1);
            }, 1000);
        }
        return () => {
            if (interval) clearInterval(interval);
        };
    }, [timerRunning]);

    useEffect(() => {
        const handleVisibilityChange = () => {
            if (document.hidden) {
                setTabSwitched(true);
            }
        };
        const handleBlur = () => {
            setTabSwitched(true);
        };
        document.addEventListener("visibilitychange", handleVisibilityChange);
        window.addEventListener("blur", handleBlur);
        return () => {
            document.removeEventListener("visibilitychange", handleVisibilityChange);
            window.removeEventListener("blur", handleBlur);
        };
    }, []);

    const isSoftSolveActive = time <= 0 || lives <= 0 || tabSwitched;

    const [sidebarOpen, setSidebarOpen] = useState(false);

    const codeRef = useRef(code);
    const activeProblemRef = useRef(activeProblem);
    const softSolvedProblemsRef = useRef(softSolvedProblems);

    useEffect(() => {
        codeRef.current = code;
    }, [code]);

    useEffect(() => {
        activeProblemRef.current = activeProblem;
    }, [activeProblem]);

    useEffect(() => {
        softSolvedProblemsRef.current = softSolvedProblems;
    }, [softSolvedProblems]);

    useEffect(() => {
        localStorage.setItem("dsa-solve-history", JSON.stringify(solveHistory));
    }, [solveHistory]);

    const todayNY = getTodayNY();
    const dailyScore = solveHistory
        .filter((entry) => entry.date === todayNY)
        .reduce((sum, entry) => {
            if (entry.difficulty === "Easy") return sum + 5;
            if (entry.difficulty === "Medium") return sum + 20;
            if (entry.difficulty === "Hard") return sum + 40;
            if (entry.difficulty === "Extreme") return sum + 1000;
            return sum;
        }, 0);

    useEffect(() => {
        const saveCode = () => {
            if (activeProblemRef.current) {
                localStorage.setItem(`dsa-code-${activeProblemRef.current.id}`, codeRef.current);
            }
        };

        window.addEventListener("beforeunload", saveCode);
        return () => {
            window.removeEventListener("beforeunload", saveCode);
            saveCode();
        };
    }, []);

    useEffect(() => {
        const handlePopState = () => {
            const slug = window.location.pathname.replace(/^\//, "");
            if (slug) {
                const prob = allProblems.find((p) => slugify(p.name) === slug);
                if (prob) {
                    if (activeProblemRef.current) {
                        localStorage.setItem(
                            `dsa-code-${activeProblemRef.current.id}`,
                            codeRef.current,
                        );
                    }
                    setActiveProblem(prob);
                    localStorage.setItem("dsa-active-problem-id", prob.id.toString());
                    const savedCode = localStorage.getItem(`dsa-code-${prob.id}`);
                    setCode(savedCode !== null ? savedCode : getTemplateCode(prob));
                }
            }
        };
        window.addEventListener("popstate", handlePopState);
        return () => window.removeEventListener("popstate", handlePopState);
    }, []);

    useEffect(() => {
        const currentSlug = window.location.pathname.replace(/^\//, "");
        const targetSlug = slugify(activeProblem.name);
        if (currentSlug !== targetSlug) {
            window.history.replaceState(null, "", `/${targetSlug}`);
        }
    }, [activeProblem]);

    const handleEditorChange = (value) => {
        setCode(value || "");
    };

    const handleSelectProblem = (newProblem) => {
        if (activeProblem) {
            localStorage.setItem(`dsa-code-${activeProblem.id}`, code);
        }
        setActiveProblem(newProblem);
        localStorage.setItem("dsa-active-problem-id", newProblem.id.toString());
        window.history.pushState(null, "", `/${slugify(newProblem.name)}`);

        const savedCode = localStorage.getItem(`dsa-code-${newProblem.id}`);
        if (savedCode !== null) {
            setCode(savedCode);
        } else {
            setCode(getTemplateCode(newProblem));
        }
        setSidebarOpen(false);
    };

    const handleResetCode = () => {
        const defaultCode = getTemplateCode(activeProblem);
        setCode(defaultCode);
        localStorage.setItem(`dsa-code-${activeProblem.id}`, defaultCode);
        setTime(getInitialTime(activeProblem.difficulty));
        setLives(3);
        setTabSwitched(false);
        setTimerRunning(true);

        setCompletedProblems((prev) => {
            const next = new Set(prev);
            next.delete(activeProblem.id);
            localStorage.setItem("dsa-completed-problems", JSON.stringify(Array.from(next)));
            return next;
        });

        setSoftSolvedProblems((prev) => {
            const next = new Set(prev);
            next.delete(activeProblem.id);
            localStorage.setItem("dsa-soft-solved-problems", JSON.stringify(Array.from(next)));
            return next;
        });
    };

    const handleResetProblemCode = (problemId) => {
        const prob = findProblemById(problemId);
        if (prob) {
            const defaultCode = getTemplateCode(prob);
            localStorage.setItem(`dsa-code-${prob.id}`, defaultCode);
            if (activeProblem.id === prob.id) {
                setCode(defaultCode);
                setTime(getInitialTime(prob.difficulty));
                setLives(3);
                setTabSwitched(false);
                setTimerRunning(true);
            }

            setCompletedProblems((prev) => {
                const next = new Set(prev);
                next.delete(prob.id);
                localStorage.setItem("dsa-completed-problems", JSON.stringify(Array.from(next)));
                return next;
            });

            setSoftSolvedProblems((prev) => {
                const next = new Set(prev);
                next.delete(prob.id);
                localStorage.setItem("dsa-soft-solved-problems", JSON.stringify(Array.from(next)));
                return next;
            });
        }
    };

    const handleResetSoftSolvedCodes = () => {
        softSolvedProblems.forEach((id) => {
            const prob = findProblemById(id);
            if (prob) {
                localStorage.setItem(`dsa-code-${id}`, getTemplateCode(prob));
            }
        });
        if (softSolvedProblems.has(activeProblem.id)) {
            setCode(getTemplateCode(activeProblem));
        }
    };

    const toggleCompleted = (id, e) => {
        e.stopPropagation();
        const nextCompleted = new Set(completedProblems);
        const nextSoft = new Set(softSolvedProblems);
        if (nextCompleted.has(id) || nextSoft.has(id)) {
            nextCompleted.delete(id);
            nextSoft.delete(id);
            setSolveHistory((prev) => prev.filter((entry) => entry.id !== id));
        } else {
            nextCompleted.add(id);
            const prob = findProblemById(id);
            if (prob) {
                const today = getTodayNY();
                setSolveHistory((prev) => {
                    const alreadySolvedToday = prev.some(
                        (entry) => entry.id === id && entry.date === today,
                    );
                    if (alreadySolvedToday) return prev;
                    return [...prev, { id, date: today, difficulty: prob.difficulty }];
                });
            }
        }
        setCompletedProblems(nextCompleted);
        setSoftSolvedProblems(nextSoft);
        localStorage.setItem("dsa-completed-problems", JSON.stringify(Array.from(nextCompleted)));
        localStorage.setItem("dsa-soft-solved-problems", JSON.stringify(Array.from(nextSoft)));
    };

    useEffect(() => {
        const handleSolved = (e) => {
            const { id, isSoft } = e.detail;
            const prob = findProblemById(id);
            if (prob) {
                const today = getTodayNY();
                setSolveHistory((prev) => {
                    const alreadySolvedToday = prev.some(
                        (entry) => entry.id === id && entry.date === today,
                    );
                    if (alreadySolvedToday) return prev;
                    return [...prev, { id, date: today, difficulty: prob.difficulty }];
                });
            }
            if (isSoft) {
                setCompletedProblems((prevCompleted) => {
                    if (prevCompleted.has(id)) return prevCompleted;
                    setSoftSolvedProblems((prevSoft) => {
                        if (prevSoft.has(id)) return prevSoft;
                        const next = new Set(prevSoft);
                        next.add(id);
                        localStorage.setItem(
                            "dsa-soft-solved-problems",
                            JSON.stringify(Array.from(next)),
                        );
                        return next;
                    });
                    return prevCompleted;
                });
                setTimerRunning(false);
            } else {
                setCompletedProblems((prev) => {
                    if (prev.has(id)) return prev;
                    const next = new Set(prev);
                    next.add(id);
                    localStorage.setItem(
                        "dsa-completed-problems",
                        JSON.stringify(Array.from(next)),
                    );
                    return next;
                });
                setSoftSolvedProblems((prev) => {
                    if (!prev.has(id)) return prev;
                    const next = new Set(prev);
                    next.delete(id);
                    localStorage.setItem(
                        "dsa-soft-solved-problems",
                        JSON.stringify(Array.from(next)),
                    );
                    return next;
                });
                setTimerRunning(false);
            }
        };
        window.addEventListener("dsa-problem-solved", handleSolved);
        return () => window.removeEventListener("dsa-problem-solved", handleSolved);
    }, []);

    useEffect(() => {
        const handleWrong = () => {
            setLives((prev) => Math.max(0, prev - 1));
        };
        window.addEventListener("dsa-problem-wrong", handleWrong);
        return () => window.removeEventListener("dsa-problem-wrong", handleWrong);
    }, []);

    const handleResetAll = () => {
        allProblems.forEach((p) => localStorage.removeItem(`dsa-code-${p.id}`));
        localStorage.removeItem("dsa-completed-problems");
        localStorage.removeItem("dsa-soft-solved-problems");
        localStorage.removeItem("dsa-solve-history");
        setCompletedProblems(new Set());
        setSoftSolvedProblems(new Set());
        setSolveHistory([]);
        setCode(getTemplateCode(activeProblem));
        localStorage.setItem(`dsa-code-${activeProblem.id}`, getTemplateCode(activeProblem));
        setTime(getInitialTime(activeProblem.difficulty));
        setLives(3);
        setTabSwitched(false);
        setTimerRunning(true);
        window.dispatchEvent(new CustomEvent("dsa-reset-all"));
    };

    const [leftWidth, setLeftWidth] = useState(35);
    const [isDraggingH, setIsDraggingH] = useState(false);
    const containerRef = useRef(null);

    const handleMouseDownH = (e) => {
        e.preventDefault();
        setIsDraggingH(true);
    };

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!isDraggingH || !containerRef.current) return;
            const containerRect = containerRef.current.getBoundingClientRect();
            const newWidth = ((e.clientX - containerRect.left) / containerRect.width) * 100;
            setLeftWidth(Math.max(25, Math.min(75, newWidth)));
        };

        const handleMouseUp = () => {
            setIsDraggingH(false);
        };

        if (isDraggingH) {
            window.addEventListener("mousemove", handleMouseMove);
            window.addEventListener("mouseup", handleMouseUp);
        }

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("mouseup", handleMouseUp);
        };
    }, [isDraggingH]);

    const [topHeight, setTopHeight] = useState(100);
    const [isDraggingV, setIsDraggingV] = useState(false);
    const rightPanelRef = useRef(null);

    const handleMouseDownV = (e) => {
        e.preventDefault();
        setIsDraggingV(true);
    };

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!isDraggingV || !rightPanelRef.current) return;
            const rect = rightPanelRef.current.getBoundingClientRect();
            const newHeight = ((e.clientY - rect.top) / rect.height) * 100;
            setTopHeight(Math.max(20, Math.min(100, newHeight)));
        };

        const handleMouseUp = () => {
            setIsDraggingV(false);
        };

        if (isDraggingV) {
            window.addEventListener("mousemove", handleMouseMove);
            window.addEventListener("mouseup", handleMouseUp);
        }

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("mouseup", handleMouseUp);
        };
    }, [isDraggingV]);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                e.preventDefault();
                e.stopPropagation();
                const isSubmit = !e.shiftKey;
                window.dispatchEvent(new CustomEvent("trigger-dsa-run", { detail: { isSubmit } }));
            } else if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === "s") {
                e.preventDefault();
                e.stopPropagation();
                if (activeProblemRef.current) {
                    fetch(`http://127.0.0.1:8000/solution/${activeProblemRef.current.id}`)
                        .then((res) => {
                            if (!res.ok) throw new Error("Failed to fetch solution");
                            return res.json();
                        })
                        .then((data) => {
                            if (data.solution) {
                                setCode(data.solution);
                                localStorage.setItem(
                                    `dsa-code-${activeProblemRef.current.id}`,
                                    data.solution,
                                );
                                setTabSwitched(true);
                            }
                        })
                        .catch((err) => {
                            console.error(err);
                        });
                }
            }
        };
        window.addEventListener("keydown", handleKeyDown, true);
        return () => window.removeEventListener("keydown", handleKeyDown, true);
    }, []);

    useEffect(() => {
        const handleTriggerRun = () => {
            setTopHeight(50);
        };
        window.addEventListener("trigger-dsa-run", handleTriggerRun);
        return () => window.removeEventListener("trigger-dsa-run", handleTriggerRun);
    }, []);

    const [isRunning, setIsRunning] = useState(false);
    useEffect(() => {
        const handleRunning = (e) => setIsRunning(e.detail.running);
        window.addEventListener("dsa-running", handleRunning);
        return () => window.removeEventListener("dsa-running", handleRunning);
    }, []);

    const consoleOpen = topHeight < 100;
    const toggleConsole = () => setTopHeight((h) => (h >= 100 ? 50 : 100));

    const isDragging = isDraggingH || isDraggingV;

    return (
        <div className="h-screen w-screen flex flex-col overflow-hidden font-sans">
            <Navbar
                key={activeProblem.id}
                onOpenSidebar={() => setSidebarOpen(true)}
                activeProblem={activeProblem}
                allProblems={allProblems}
                completedCount={completedProblems.size}
                totalCount={allProblems.length}
                onResetCode={handleResetCode}
                onSelectProblem={handleSelectProblem}
                time={time}
                timerRunning={timerRunning}
                setTimerRunning={setTimerRunning}
                lives={lives}
                isSoftSolveActive={isSoftSolveActive}
                dailyScore={dailyScore}
                isHardSolved={completedProblems.has(activeProblem.id)}
            />

            <Sidebar
                sidebarOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                allProblems={allProblems}
                completedProblems={completedProblems}
                softSolvedProblems={softSolvedProblems}
                activeProblem={activeProblem}
                onSelectProblem={handleSelectProblem}
                onToggleCompleted={toggleCompleted}
                onResetAll={handleResetAll}
                onResetSoftCodes={handleResetSoftSolvedCodes}
                onResetProblemCode={handleResetProblemCode}
            />

            <main
                ref={containerRef}
                className={`flex-1 min-h-0 flex bg-zinc-800 relative z-10 ${isDragging ? "select-none" : ""} ${isDraggingH ? "cursor-col-resize" : ""} ${isDraggingV ? "cursor-row-resize" : ""}`}
            >
                <div
                    style={{ width: `${leftWidth}%` }}
                    className="h-full flex flex-col min-h-0 relative"
                >
                    <ProblemDescription activeProblem={activeProblem} />
                </div>

                <div
                    onMouseDown={handleMouseDownH}
                    className="w-1.5 h-full cursor-col-resize bg-[#1e1e1e] hover:bg-zinc-600 transition-colors shrink-0 z-10"
                />

                <div
                    style={{ width: `${100 - leftWidth}%` }}
                    className={`h-full flex flex-col min-h-0 relative ${isDragging ? "pointer-events-none" : ""}`}
                >
                    <div ref={rightPanelRef} className="flex-1 min-h-0 flex flex-col">
                        <div
                            style={{ height: consoleOpen ? `${topHeight}%` : "100%" }}
                            className="min-h-0 relative"
                        >
                            <Editor value={code} onChange={handleEditorChange} />
                        </div>

                        {consoleOpen && (
                            <div
                                onMouseDown={handleMouseDownV}
                                onDoubleClick={() => setTopHeight(100)}
                                className="h-2 w-full cursor-row-resize bg-[#1a1a1a] border-t border-zinc-800 hover:bg-zinc-600 transition-colors shrink-0 z-10"
                            />
                        )}

                        <div
                            style={{ height: consoleOpen ? `${100 - topHeight}%` : "0%" }}
                            className={`min-h-0 ${consoleOpen ? "" : "hidden"}`}
                        >
                            <BottomPanel
                                key={activeProblem.id}
                                activeProblem={activeProblem}
                                code={code}
                                isSoftSolveActive={isSoftSolveActive}
                            />
                        </div>
                    </div>

                    <div className="flex items-center justify-between px-3 py-1.5 bg-[#1e1e1e] border-t border-zinc-800 shrink-0">
                        <button
                            onClick={toggleConsole}
                            className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors cursor-pointer focus:outline-none"
                        >
                            <span>Console</span>
                            <svg
                                className="w-3.5 h-3.5"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                {consoleOpen ? (
                                    <path d="m6 9 6 6 6-6" />
                                ) : (
                                    <path d="m18 15-6-6-6 6" />
                                )}
                            </svg>
                        </button>
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() =>
                                    window.dispatchEvent(
                                        new CustomEvent("trigger-dsa-run", {
                                            detail: { isSubmit: false },
                                        }),
                                    )
                                }
                                disabled={isRunning}
                                className="px-4 py-1.5 text-sm font-medium bg-zinc-700 hover:bg-zinc-600 text-zinc-200 rounded transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none"
                            >
                                {isRunning ? "Running..." : "Run"}
                            </button>
                            <button
                                onClick={() =>
                                    window.dispatchEvent(
                                        new CustomEvent("trigger-dsa-run", {
                                            detail: { isSubmit: true },
                                        }),
                                    )
                                }
                                disabled={isRunning}
                                className="px-4 py-1.5 text-sm font-semibold bg-emerald-600 hover:bg-emerald-500 text-white rounded transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none"
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                </div>
                {activeProblem.difficulty === "Extreme" && (
                    <>
                        <div className="evil-overlay" />
                        <div className="ember-container">
                            {embers.map((emb) => (
                                <div
                                    key={emb.id}
                                    className="ember"
                                    style={{
                                        left: emb.left,
                                        bottom: emb.bottom,
                                        width: emb.size,
                                        height: emb.size,
                                        animationDuration: emb.duration,
                                        animationDelay: emb.delay,
                                        "--tx": emb.tx,
                                        "--ty": emb.ty,
                                        "--rot": emb.rot,
                                    }}
                                />
                            ))}
                        </div>
                    </>
                )}
            </main>
        </div>
    );
}

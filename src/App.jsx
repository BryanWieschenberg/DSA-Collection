import { useState, useEffect, useRef } from "react";
import Editor from "./components/Editor";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import ProblemDescription from "./components/ProblemDescription";
import BottomPanel from "./components/BottomPanel";
import { getTemplateCode, slugify, findProblemById, allProblems } from "./lib/appHelpers";

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

    const [code, setCode] = useState(() => {
        const savedCode = localStorage.getItem(`dsa-code-${activeProblem.id}`);
        if (savedCode !== null) return savedCode;
        return getTemplateCode(activeProblem);
    });

    const [completedProblems, setCompletedProblems] = useState(() => {
        const saved = localStorage.getItem("dsa-completed-problems");
        return saved ? new Set(JSON.parse(saved)) : new Set();
    });

    const [sidebarOpen, setSidebarOpen] = useState(false);

    const codeRef = useRef(code);
    const activeProblemRef = useRef(activeProblem);

    useEffect(() => {
        codeRef.current = code;
    }, [code]);

    useEffect(() => {
        activeProblemRef.current = activeProblem;
    }, [activeProblem]);

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
    };

    const toggleCompleted = (id, e) => {
        e.stopPropagation();
        const next = new Set(completedProblems);
        if (next.has(id)) {
            next.delete(id);
        } else {
            next.add(id);
        }
        setCompletedProblems(next);
        localStorage.setItem("dsa-completed-problems", JSON.stringify(Array.from(next)));
    };

    const [leftWidth, setLeftWidth] = useState(50);
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
                window.dispatchEvent(
                    new CustomEvent("trigger-dsa-run", { detail: { isSubmit } })
                );
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
            />

            <Sidebar
                sidebarOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                allProblems={allProblems}
                completedProblems={completedProblems}
                activeProblem={activeProblem}
                onSelectProblem={handleSelectProblem}
                onToggleCompleted={toggleCompleted}
            />

            <main
                ref={containerRef}
                className={`flex-1 min-h-0 flex bg-zinc-800 ${isDragging ? "select-none" : ""} ${isDraggingH ? "cursor-col-resize" : ""} ${isDraggingV ? "cursor-row-resize" : ""}`}
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
                    ref={rightPanelRef}
                    style={{ width: `${100 - leftWidth}%` }}
                    className={`h-full flex flex-col min-h-0 relative ${isDragging ? "pointer-events-none" : ""}`}
                >
                    <div style={{ height: `${topHeight}%` }} className="min-h-0 relative">
                        <Editor value={code} onChange={handleEditorChange} />
                    </div>

                    <div
                        onMouseDown={handleMouseDownV}
                        onDoubleClick={() => setTopHeight(100)}
                        className="h-1.5 w-full cursor-row-resize bg-[#1e1e1e] hover:bg-zinc-600 transition-colors shrink-0 z-10"
                    />

                    <div style={{ height: `${100 - topHeight}%` }} className="min-h-0">
                        <BottomPanel key={activeProblem.id} activeProblem={activeProblem} />
                    </div>
                </div>
            </main>
        </div>
    );
}

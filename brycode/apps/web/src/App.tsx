import { useState, useCallback, useRef, useEffect } from "react";
import ProblemDescription from "./components/ProblemDescription";
import CodeEditor from "./components/CodeEditor";
import OutputPanel from "./components/OutputPanel";
import type { OutputPanelHandle } from "./components/OutputPanel";
import { twoSum } from "./data/problems";

function App() {
  const problem = twoSum;
  const [code, setCode] = useState(problem.starterCode);
  const outputRef = useRef<OutputPanelHandle>(null);

  // --- Resizable panels ---
  const containerRef = useRef<HTMLDivElement>(null);
  const [leftWidth, setLeftWidth] = useState(40); // percentage
  const [topHeight, setTopHeight] = useState(60); // percentage of right panel
  const dragging = useRef<"horizontal" | "vertical" | null>(null);

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();

      if (dragging.current === "horizontal") {
        const pct = ((e.clientX - rect.left) / rect.width) * 100;
        setLeftWidth(Math.max(25, Math.min(65, pct)));
      } else if (dragging.current === "vertical") {
        const rightPanelLeft = rect.left + (rect.width * leftWidth) / 100 + 5;
        const rightPanelHeight = rect.height;
        const relY = e.clientY - rect.top;
        const pct = (relY / rightPanelHeight) * 100;
        setTopHeight(Math.max(25, Math.min(80, pct)));
      }
    },
    [leftWidth]
  );

  const handleMouseUp = useCallback(() => {
    dragging.current = null;
    document.body.style.cursor = "";
    document.body.style.userSelect = "";
  }, []);

  useEffect(() => {
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [handleMouseMove, handleMouseUp]);

  const handleSubmit = useCallback(() => {
    outputRef.current?.handleSubmit();
  }, []);

  const startDrag = (dir: "horizontal" | "vertical") => {
    dragging.current = dir;
    document.body.style.cursor = dir === "horizontal" ? "col-resize" : "row-resize";
    document.body.style.userSelect = "none";
  };

  return (
    <div className="flex flex-col h-screen bg-surface-900">
      {/* Top navbar */}
      <nav className="flex items-center justify-between px-5 h-12 border-b border-border bg-surface-800/80 backdrop-blur-sm flex-shrink-0">
        <div className="flex items-center gap-3">
          {/* Logo */}
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-accent to-accent-bright flex items-center justify-center shadow-[0_0_20px_rgba(124,92,252,0.3)]">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            <span className="text-[15px] font-bold tracking-tight text-text-primary">
              Bry<span className="text-accent-bright">Code</span>
            </span>
          </div>

          {/* Divider */}
          <div className="w-px h-5 bg-border" />

          {/* Problem nav */}
          <div className="flex items-center gap-1.5">
            <button
              id="btn-prev-problem"
              className="p-1.5 rounded-md hover:bg-surface-600 text-text-muted hover:text-text-secondary transition-all cursor-pointer"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <span className="text-[13px] font-medium text-text-secondary px-2">
              Problem List
            </span>
            <button
              id="btn-next-problem"
              className="p-1.5 rounded-md hover:bg-surface-600 text-text-muted hover:text-text-secondary transition-all cursor-pointer"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        {/* Right side — timer / settings placeholder */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-600 border border-border text-text-muted">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-[12px] font-mono font-medium">00:00</span>
          </div>
          <button
            id="btn-settings"
            className="p-2 rounded-lg hover:bg-surface-600 text-text-muted hover:text-text-secondary transition-all cursor-pointer"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </nav>

      {/* Main content area */}
      <div ref={containerRef} className="flex flex-1 overflow-hidden">
        {/* Left — Problem Description */}
        <div style={{ width: `${leftWidth}%` }} className="flex-shrink-0 overflow-hidden">
          <ProblemDescription problem={problem} />
        </div>

        {/* Horizontal resizer */}
        <div
          className="resizer resizer-horizontal bg-surface-900"
          onMouseDown={() => startDrag("horizontal")}
        />

        {/* Right — Editor + Output */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Top — Code Editor */}
          <div style={{ height: `${topHeight}%` }} className="flex-shrink-0 overflow-hidden">
            <CodeEditor code={code} onChange={setCode} onSubmit={handleSubmit} />
          </div>

          {/* Vertical resizer */}
          <div
            className="resizer resizer-vertical bg-surface-900"
            onMouseDown={() => startDrag("vertical")}
          />

          {/* Bottom — Output */}
          <div className="flex-1 overflow-hidden">
            <OutputPanel ref={outputRef} problem={problem} code={code} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

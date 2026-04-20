import { useState, useImperativeHandle, forwardRef, useCallback } from "react";
import type { Problem } from "../data/problems";
import SuccessAnimation from "./SuccessAnimation";

const API_BASE = "http://localhost:8000";

interface TestResult {
  id: number;
  input: string;
  expected: string;
  actual: string | null;
  passed: boolean | null;
  error: string | null;
  stdout: string | null;
}

export interface OutputPanelHandle {
  handleRun: () => void;
  handleSubmit: () => void;
}

interface OutputPanelProps {
  problem: Problem;
  code: string;
}

const OutputPanel = forwardRef<OutputPanelHandle, OutputPanelProps>(
  ({ problem, code }, ref) => {
    const [activeTab, setActiveTab] = useState<"testcases" | "result">("testcases");
    const [activeCase, setActiveCase] = useState(0);
    const [loading, setLoading] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);
    const [results, setResults] = useState<TestResult[]>(
      problem.testCases.map((tc, i) => ({
        id: i,
        input: tc.input,
        expected: tc.expected,
        actual: null,
        passed: null,
        error: null,
        stdout: null,
      }))
    );

    const currentResult = results[activeCase];

    const handleRun = useCallback(async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/run/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            slug: problem.slug,
            code,
            test_indices: [activeCase],
          }),
        });
        const data = await res.json();

        setResults((prev) =>
          prev.map((r) => {
            const match = data.results.find(
              (dr: { index: number }) => dr.index === r.id
            );
            if (!match) return r;
            return {
              ...r,
              actual: match.actual,
              passed: match.passed,
              error: match.error,
              stdout: match.stdout,
            };
          })
        );
        setActiveTab("testcases");
      } catch {
        setResults((prev) =>
          prev.map((r, i) =>
            i === activeCase
              ? { ...r, actual: null, passed: false, error: "Failed to connect to server", stdout: null }
              : r
          )
        );
      } finally {
        setLoading(false);
      }
    }, [problem.slug, code, activeCase]);

    const handleSubmit = useCallback(async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/run/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            slug: problem.slug,
            code,
          }),
        });
        const data = await res.json();

        setResults((prev) =>
          prev.map((r) => {
            const match = data.results.find(
              (dr: { index: number }) => dr.index === r.id
            );
            if (!match) return r;
            return {
              ...r,
              actual: match.actual,
              passed: match.passed,
              error: match.error,
              stdout: match.stdout,
            };
          })
        );
        setActiveTab("testcases");

        // Check if all passed
        if (data.results.length > 0 && data.results.every((r: { passed: boolean }) => r.passed)) {
          setShowSuccess(true);
        }
      } catch {
        setResults((prev) =>
          prev.map((r) => ({
            ...r,
            actual: null,
            passed: false,
            error: "Failed to connect to server",
            stdout: null,
          }))
        );
      } finally {
        setLoading(false);
      }
    }, [problem.slug, code]);

    // Expose run/submit to parent via ref
    useImperativeHandle(ref, () => ({ handleRun, handleSubmit }), [handleRun, handleSubmit]);

    return (
      <>
      <SuccessAnimation show={showSuccess} onComplete={() => setShowSuccess(false)} />
      <div className="flex flex-col h-full bg-surface-800 overflow-hidden">
        {/* Tab bar */}
        <div className="flex items-center justify-between px-4 pt-2 pb-0 border-b border-border">
          <div className="flex items-center gap-1">
            <button
              id="tab-testcases"
              onClick={() => setActiveTab("testcases")}
              className={`px-3 py-2 text-[12px] font-medium rounded-t-lg transition-all duration-200 cursor-pointer ${
                activeTab === "testcases"
                  ? "bg-surface-700 text-text-primary border border-border border-b-transparent -mb-px"
                  : "text-text-muted hover:text-text-secondary"
              }`}
            >
              Test Cases
            </button>
            <button
              id="tab-result"
              onClick={() => setActiveTab("result")}
              className={`px-3 py-2 text-[12px] font-medium rounded-t-lg transition-all duration-200 cursor-pointer ${
                activeTab === "result"
                  ? "bg-surface-700 text-text-primary border border-border border-b-transparent -mb-px"
                  : "text-text-muted hover:text-text-secondary"
              }`}
            >
              Result
            </button>
          </div>

          {/* Run / Submit buttons */}
          <div className="flex items-center gap-2 pb-1">
            <button
              id="btn-run"
              onClick={handleRun}
              disabled={loading}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-surface-500 hover:bg-surface-400 text-text-primary text-[12px] font-semibold transition-all duration-200 cursor-pointer border border-border hover:border-border-bright disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              ) : (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              )}
              Run
            </button>
            <button
              id="btn-submit"
              onClick={handleSubmit}
              disabled={loading}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-green/90 hover:bg-green text-surface-900 text-[12px] font-bold transition-all duration-200 cursor-pointer shadow-[0_0_20px_rgba(74,222,128,0.15)] hover:shadow-[0_0_20px_rgba(74,222,128,0.3)] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              ) : (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              )}
              Submit
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === "testcases" ? (
            <div className="space-y-4">
              {/* Case selector pills */}
              <div className="flex items-center gap-2">
                {results.map((r, i) => {
                  const statusColor =
                    r.passed === null
                      ? "bg-surface-500 text-text-secondary border-border"
                      : r.passed
                      ? "bg-green-dim text-green border-green/30"
                      : "bg-red-dim text-red border-red/30";

                  return (
                    <button
                      key={i}
                      id={`case-${i}`}
                      onClick={() => setActiveCase(i)}
                      className={`px-3 py-1.5 rounded-lg text-[12px] font-medium border transition-all duration-200 cursor-pointer ${statusColor} ${
                        activeCase === i
                          ? "ring-1 ring-accent/50"
                          : "opacity-70 hover:opacity-100"
                      }`}
                    >
                      Case {i + 1}
                    </button>
                  );
                })}
              </div>

              {/* Active case details */}
              {currentResult && (
                <div className="space-y-3">
                  {/* Input */}
                  <div className="space-y-1.5">
                    <label className="text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                      Input
                    </label>
                    <div className="rounded-lg bg-surface-700 border border-border p-3 font-mono text-[13px] text-text-primary">
                      {currentResult.input}
                    </div>
                  </div>

                  {/* Expected Output */}
                  <div className="space-y-1.5">
                    <label className="text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                      Expected Output
                    </label>
                    <div className="rounded-lg bg-surface-700 border border-border p-3 font-mono text-[13px] text-green">
                      {currentResult.expected}
                    </div>
                  </div>

                  {/* Your Output */}
                  {currentResult.actual !== null && (
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                        Your Output
                      </label>
                      <div
                        className={`rounded-lg bg-surface-700 border p-3 font-mono text-[13px] ${
                          currentResult.passed
                            ? "border-green/30 text-green"
                            : "border-red/30 text-red"
                        }`}
                      >
                        {currentResult.actual}
                      </div>
                    </div>
                  )}

                  {/* Console Output (stdout) */}
                  {currentResult.stdout && (
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                        Console Output
                      </label>
                      <div className="rounded-lg bg-surface-700 border border-border p-3 font-mono text-[13px] text-yellow whitespace-pre-wrap">
                        {currentResult.stdout}
                      </div>
                    </div>
                  )}

                  {/* Error */}
                  {currentResult.error && (
                    <div className="space-y-1.5">
                      <label className="text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                        Error
                      </label>
                      <div className="rounded-lg bg-red-dim border border-red/20 p-3 font-mono text-[13px] text-red whitespace-pre-wrap">
                        {currentResult.error}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-text-muted">
              <svg className="w-10 h-10 mb-3 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-sm font-medium">Run your code to see results</p>
              <p className="text-xs mt-1 text-text-muted/60">
                Click Run or press Ctrl + Enter
              </p>
            </div>
          )}
        </div>
      </div>
      </>
    );
  }
);

OutputPanel.displayName = "OutputPanel";
export default OutputPanel;

import { useState } from "react";
import type { Problem } from "../data/problems";

interface ProblemDescriptionProps {
  problem: Problem;
}

export default function ProblemDescription({ problem }: ProblemDescriptionProps) {
  const [activeTab, setActiveTab] = useState<"description" | "solutions">("description");

  const difficultyColor = {
    Easy: "text-green bg-green-dim",
    Medium: "text-yellow bg-yellow-dim",
    Hard: "text-red bg-red-dim",
  }[problem.difficulty];

  return (
    <div className="flex flex-col h-full bg-surface-800 overflow-hidden">
      {/* Tab bar */}
      <div className="flex items-center gap-1 px-4 pt-3 pb-0 border-b border-border">
        <button
          id="tab-description"
          onClick={() => setActiveTab("description")}
          className={`px-4 py-2.5 text-[13px] font-medium rounded-t-lg transition-all duration-200 cursor-pointer ${
            activeTab === "description"
              ? "bg-surface-700 text-text-primary border border-border border-b-transparent -mb-px"
              : "text-text-muted hover:text-text-secondary"
          }`}
        >
          Description
        </button>
        <button
          id="tab-solutions"
          onClick={() => setActiveTab("solutions")}
          className={`px-4 py-2.5 text-[13px] font-medium rounded-t-lg transition-all duration-200 cursor-pointer ${
            activeTab === "solutions"
              ? "bg-surface-700 text-text-primary border border-border border-b-transparent -mb-px"
              : "text-text-muted hover:text-text-secondary"
          }`}
        >
          Solutions
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {activeTab === "description" ? (
          <div className="space-y-6">
            {/* Title + Difficulty */}
            <div className="space-y-3">
              <h1 className="text-2xl font-bold text-text-primary tracking-tight">
                {problem.id}. {problem.title}
              </h1>
              <div className="flex items-center gap-3">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${difficultyColor}`}
                >
                  {problem.difficulty}
                </span>
              </div>
            </div>

            {/* Description */}
            <div
              className="text-[15px] leading-relaxed text-text-secondary [&_code]:bg-surface-500 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-accent-bright [&_code]:text-[13px] [&_code]:font-mono [&_em]:text-text-primary [&_em]:not-italic [&_strong]:text-text-primary"
              dangerouslySetInnerHTML={{ __html: problem.description }}
            />

            {/* Examples */}
            <div className="space-y-4">
              {problem.examples.map((example) => (
                <div
                  key={example.id}
                  className="rounded-xl border border-border bg-surface-700/50 overflow-hidden"
                >
                  <div className="px-4 py-2.5 bg-surface-700 border-b border-border">
                    <span className="text-[13px] font-semibold text-text-secondary">
                      Example {example.id}
                    </span>
                  </div>
                  <div className="p-4 space-y-2 font-mono text-[13px]">
                    <div>
                      <span className="text-text-muted">Input: </span>
                      <span className="text-text-primary">{example.input}</span>
                    </div>
                    <div>
                      <span className="text-text-muted">Output: </span>
                      <span className="text-green">{example.output}</span>
                    </div>
                    {example.explanation && (
                      <div className="pt-1">
                        <span className="text-text-muted">Explanation: </span>
                        <span className="text-text-secondary">
                          {example.explanation}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Constraints */}
            <div className="space-y-3">
              <h3 className="text-[15px] font-semibold text-text-primary">
                Constraints:
              </h3>
              <ul className="space-y-2">
                {problem.constraints.map((c, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2.5 text-[14px] text-text-secondary [&_code]:bg-surface-500 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-accent-bright [&_code]:text-[12px] [&_code]:font-mono"
                  >
                    <span className="text-accent mt-1.5 text-[8px]">●</span>
                    <span dangerouslySetInnerHTML={{ __html: c }} />
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-text-muted">
            <svg className="w-12 h-12 mb-4 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.331 0 4.467.89 6.063 2.348m0-16.306A8.967 8.967 0 0118 3.75c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6.063 2.348m0-16.306v16.306" />
            </svg>
            <p className="text-sm font-medium">Solutions coming soon</p>
            <p className="text-xs mt-1 text-text-muted/60">Solve it yourself first!</p>
          </div>
        )}
      </div>
    </div>
  );
}

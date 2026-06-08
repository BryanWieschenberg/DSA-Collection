import { renderMarkdown } from "./RenderMarkdown";
import { compactValue, pythonize } from "../lib/appHelpers";

const VALUE_TOKEN =
    /("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:true|false|null|True|False|None)\b|-?\d+(?:\.\d+)?)/g;

const highlightValue = (text) => {
    if (!text) return text;
    return text.split(VALUE_TOKEN).map((part, i) => {
        if (!part) return null;
        const c = part[0];
        if (c === '"' || c === "'") {
            return (
                <span key={i} style={{ color: "#CE9178" }}>
                    {part}
                </span>
            );
        }
        if (/^(true|false|null|True|False|None)$/.test(part)) {
            return (
                <span key={i} style={{ color: "#569CD6" }}>
                    {part}
                </span>
            );
        }
        if (/^-?\d/.test(part)) {
            return (
                <span key={i} style={{ color: "#B5CEA8" }}>
                    {part}
                </span>
            );
        }
        return part;
    });
};

export default function ProblemDescription({ activeProblem }) {
    const { description, examples, constraints } = activeProblem;

    return (
        <div className="w-full h-full bg-zinc-900/30 overflow-y-auto p-8 select-text space-y-6 desc-scrollbar">
            <div className="text-zinc-100 text-[15px] leading-relaxed whitespace-pre-wrap">
                {renderMarkdown(description)}
            </div>

            {examples && examples.length > 0 && (
                <div className="space-y-5">
                    {examples.map((ex, idx) => (
                        <div key={idx} className="space-y-2">
                            <h3 className="text-base font-semibold text-zinc-100">
                                Example {idx + 1}:
                            </h3>
                            <div className="bg-zinc-900/40 border border-zinc-800/60 rounded-xl p-4">
                                <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                    <div className="flex gap-2">
                                        <span className="shrink-0 select-none">
                                            <span style={{ color: "#34D399" }}>Input</span>
                                            <span className="text-zinc-200">:</span>
                                        </span>
                                        <span className="text-zinc-200">
                                            {highlightValue(compactValue(pythonize(ex.input)))}
                                        </span>
                                    </div>
                                    <div className="flex gap-2">
                                        <span className="shrink-0 select-none">
                                            <span style={{ color: "#34D399" }}>Output</span>
                                            <span className="text-zinc-200">:</span>
                                        </span>
                                        <span className="text-zinc-200">
                                            {highlightValue(compactValue(pythonize(ex.output)))}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            {ex.explanation && (
                                <div className="text-zinc-100 text-[15px] leading-relaxed whitespace-pre-wrap">
                                    <div className="text-zinc-400">Explanation:</div>
                                    <div className="mt-1">{renderMarkdown(ex.explanation)}</div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {constraints && constraints.length > 0 && (
                <div className="space-y-3 pt-2">
                    <h3 className="text-base font-semibold text-zinc-100">Constraints:</h3>
                    <ul className="space-y-3 pl-4 text-zinc-100 text-[15px] leading-relaxed">
                        {constraints.map((c, idx) => (
                            <li key={idx} className="flex gap-3.5">
                                <span className="select-none shrink-0">•</span>
                                <div className="flex-1">{renderMarkdown(c)}</div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

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
                    {examples.map((ex, idx) => {
                        let isClassLayout = false;
                        let parsedInput = null;
                        let parsedOutput = null;
                        if (activeProblem.code && activeProblem.code.trim().startsWith("class ")) {
                            try {
                                parsedInput = JSON.parse(ex.input);
                                parsedOutput = JSON.parse(ex.output);
                                if (
                                    Array.isArray(parsedInput) &&
                                    Array.isArray(parsedOutput) &&
                                    parsedInput.length === parsedOutput.length
                                ) {
                                    isClassLayout = true;
                                }
                            } catch (e) {
                                isClassLayout = false;
                            }
                        }

                        return (
                            <div key={idx} className="space-y-2">
                                <h3 className="text-base font-semibold text-zinc-100">
                                    Example {idx + 1}:
                                </h3>
                                <div className="bg-zinc-900/40 border border-zinc-800/60 rounded-xl p-4">
                                    {isClassLayout ? (
                                        <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                            <div className="grid grid-cols-2 gap-4 pb-1 mb-1 border-zinc-800/40 select-none">
                                                <div>
                                                    <span style={{ color: "#34D399" }}>Input</span>
                                                    <span className="text-zinc-200">:</span>
                                                </div>
                                                <div>
                                                    <span style={{ color: "#34D399" }}>Output</span>
                                                    <span className="text-zinc-200">:</span>
                                                </div>
                                            </div>
                                            {parsedInput.map((call, i) => {
                                                const [methodName, args] = call;
                                                const argsStr = args
                                                    .map((arg) =>
                                                        compactValue(
                                                            pythonize(JSON.stringify(arg)),
                                                        ),
                                                    )
                                                    .join(", ");
                                                const formattedCall = `${methodName}(${argsStr})`;
                                                const retVal = parsedOutput[i];
                                                const formattedRet = compactValue(
                                                    pythonize(JSON.stringify(retVal)),
                                                );
                                                return (
                                                    <div key={i} className="grid grid-cols-2 gap-4">
                                                        <div className="text-zinc-200">
                                                            {highlightValue(formattedCall)}
                                                        </div>
                                                        <div className="text-zinc-200">
                                                            {highlightValue(formattedRet)}
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    ) : (
                                        <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                            <div className="whitespace-pre-wrap">
                                                <span className="select-none" style={{ color: "#34D399" }}>Input: </span>
                                                <span className="text-zinc-200">
                                                    {highlightValue(
                                                        compactValue(pythonize(ex.input)),
                                                    )}
                                                </span>
                                            </div>
                                            <div className="whitespace-pre-wrap">
                                                <span className="select-none" style={{ color: "#34D399" }}>Output: </span>
                                                <span className="text-zinc-200">
                                                    {highlightValue(
                                                        compactValue(pythonize(ex.output)),
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    )}
                                </div>
                                {ex.explanation && (
                                    <div className="text-zinc-300 text-[15px] leading-relaxed whitespace-pre-wrap [&_p]:inline">
                                        <span className="font-normal text-zinc-100">
                                            Explanation:{" "}
                                        </span>
                                        {renderMarkdown(ex.explanation)}
                                    </div>
                                )}
                            </div>
                        );
                    })}
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

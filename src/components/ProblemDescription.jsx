export default function ProblemDescription({ activeProblem }) {
    const { description, examples, constraints } = activeProblem;

    const renderMarkdown = (text) => {
        if (!text) return "";
        const lines = text.split("\n");
        return lines.map((line, lineIdx) => {
            const parts = line.split("`");
            const renderedLine = parts.map((part, index) => {
                if (index % 2 === 1) {
                    return (
                        <code
                            key={index}
                            className="bg-zinc-800/80 text-zinc-200 px-1 py-0.5 rounded font-mono text-sm border border-zinc-700/40"
                        >
                            {part}
                        </code>
                    );
                }
                const boldParts = part.split("**");
                return boldParts.map((subPart, subIndex) => {
                    if (subIndex % 2 === 1) {
                        return (
                            <strong key={subIndex} className="font-bold text-zinc-100">
                                {subPart}
                            </strong>
                        );
                    }
                    const italicParts = subPart.split("*");
                    return italicParts.map((item, itemIdx) => {
                        if (itemIdx % 2 === 1) {
                            return (
                                <em key={itemIdx} className="italic text-zinc-400">
                                    {item}
                                </em>
                            );
                        }
                        return item;
                    });
                });
            });

            return (
                <p key={lineIdx} className={lineIdx > 0 ? "mt-3" : ""}>
                    {renderedLine}
                </p>
            );
        });
    };

    return (
        <div className="w-full h-full bg-zinc-900/30 overflow-y-auto p-4 select-text space-y-6 desc-scrollbar">
            <div className="text-zinc-300 text-[15px] leading-relaxed whitespace-pre-wrap">
                {renderMarkdown(description)}
            </div>

            {examples && examples.length > 0 && (
                <div className="space-y-4">
                    <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">
                        Examples
                    </h3>
                    {examples.map((ex, idx) => (
                        <div
                            key={idx}
                            className="bg-zinc-900/40 border border-zinc-800/60 rounded-xl p-4 space-y-2.5"
                        >
                            <div className="text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">
                                Example {idx + 1}
                            </div>
                            <div className="space-y-1.5 font-mono text-sm text-zinc-300">
                                <div className="flex gap-2">
                                    <span className="text-zinc-500 font-bold shrink-0 select-none">
                                        Input:
                                    </span>
                                    <span className="text-zinc-200">{ex.input}</span>
                                </div>
                                <div className="flex gap-2">
                                    <span className="text-zinc-500 font-bold shrink-0 select-none">
                                        Output:
                                    </span>
                                    <span className="text-zinc-200">{ex.output}</span>
                                </div>
                                {ex.explanation && (
                                    <div className="flex gap-2 pt-2 border-t border-zinc-800/60 mt-1.5">
                                        <span className="text-zinc-500 font-bold shrink-0 select-none">
                                            Explanation:
                                        </span>
                                        <span className="text-zinc-400 font-sans leading-relaxed">
                                            {ex.explanation}
                                        </span>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {constraints && constraints.length > 0 && (
                <div className="space-y-3 pt-2">
                    <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">
                        Constraints
                    </h3>
                    <ul className="list-disc pl-5 space-y-2 text-sm text-zinc-400">
                        {constraints.map((c, idx) => (
                            <li key={idx} className="leading-relaxed">
                                {renderMarkdown(c)}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

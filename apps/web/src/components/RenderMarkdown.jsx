const formatMathText = (str) => {
    return str
        .replace(/\\times/g, "×")
        .replace(/\\lfloor/g, "⌊")
        .replace(/\\rfloor/g, "⌋")
        .replace(/\\lceil/g, "⌈")
        .replace(/\\rceil/g, "⌉")
        .replace(/\\le/g, "≤")
        .replace(/\\ge/g, "≥");
};

export const renderMarkdown = (text) => {
    if (!text) return "";
    const lines = text.split("\n");
    return lines.map((line, lineIdx) => {
        const bulletMatch = line.match(/^(\s*)(?:-\s+|\*\s+)(.*)/);
        const textToProcess = bulletMatch ? bulletMatch[2] : line;

        const parts = textToProcess.split("`");
        const renderedLine = parts.map((part, index) => {
            if (index % 2 === 1) {
                return (
                    <code
                        key={index}
                        className="bg-zinc-700/60 text-gray-200 px-1.5 py-0.5 rounded font-mono text-sm border border-zinc-600/50"
                    >
                        {part}
                    </code>
                );
            }

            const doubleDollarParts = part.split("$$");
            return doubleDollarParts.map((ddPart, ddIdx) => {
                if (ddIdx % 2 === 1) {
                    return (
                        <div
                            key={`dd-${ddIdx}`}
                            className="my-3 text-center font-serif text-lg text-zinc-200/90 bg-zinc-800/20 py-2 rounded border border-zinc-700/30"
                        >
                            {formatMathText(ddPart)}
                        </div>
                    );
                }

                const dollarParts = ddPart.split("$");
                return dollarParts.map((dPart, dIdx) => {
                    if (dIdx % 2 === 1) {
                        return (
                            <span
                                key={`d-${dIdx}`}
                                className="font-serif italic text-zinc-100/90 mx-0.5"
                            >
                                {formatMathText(dPart)}
                            </span>
                        );
                    }

                    const boldParts = dPart.split("**");
                    return boldParts.map((subPart, subIndex) => {
                        if (subIndex % 2 === 1) {
                            return (
                                <strong key={`b-${subIndex}`} className="font-bold text-zinc-100">
                                    {subPart}
                                </strong>
                            );
                        }
                        const italicParts = subPart.split("*");
                        return italicParts.map((item, itemIdx) => {
                            if (itemIdx % 2 === 1) {
                                return (
                                    <em key={`i-${itemIdx}`} className="italic">
                                        {item}
                                    </em>
                                );
                            }
                            return item;
                        });
                    });
                });
            });
        });

        if (bulletMatch) {
            const indent = bulletMatch[1].length;
            const plClass = indent >= 2 ? "pl-8" : "pl-4";
            return (
                <div
                    key={lineIdx}
                    className={`flex gap-3.5 ${plClass} ${lineIdx > 0 ? "mt-3" : ""}`}
                >
                    <span className="select-none shrink-0">•</span>
                    <div className="flex-1">{renderedLine}</div>
                </div>
            );
        }

        return (
            <p key={lineIdx} className={lineIdx > 0 ? "mt-3" : ""}>
                {renderedLine}
            </p>
        );
    });
};

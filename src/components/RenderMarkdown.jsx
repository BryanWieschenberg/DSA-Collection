export const renderMarkdown = (text) => {
    if (!text) return "";
    const lines = text.split("\n");
    return lines.map((line, lineIdx) => {
        const parts = line.split("`");
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
                            <em key={itemIdx} className="italic">
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

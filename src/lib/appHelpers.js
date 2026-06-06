import problemsData from "./problems.json";

export const getTemplateCode = (problem) => {
    const rawCode = problem.code;
    if (rawCode.trim().startsWith("class")) {
        return rawCode;
    }
    return `def ${rawCode}:\n    `;
};

export const slugify = (name) => {
    return name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "");
};

export const findProblemById = (id) => {
    for (const cat of problemsData) {
        const found = cat.problems.find((p) => p.id === id);
        if (found) return found;
    }
    return null;
};

export const allProblems = problemsData.flatMap((cat) => cat.problems);

export const DEFAULT_TIME_LIMIT_MS = 3000;
export const DEFAULT_MEMORY_LIMIT_MB = 256;

export const getLimits = (problem) => ({
    timeLimitMs: problem.timeLimit ?? DEFAULT_TIME_LIMIT_MS,
    memLimitMb: problem.memoryLimit ?? DEFAULT_MEMORY_LIMIT_MB,
});

export const getHiddenTests = (problem) =>
    Array.isArray(problem.hiddenTests) ? problem.hiddenTests : [];

export const pythonize = (text) => {
    if (!text) return text;
    return text.replace(
        /"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:true|false|null)\b/g,
        (match) => {
            if (match[0] === '"' || match[0] === "'") return match;
            return match === "true" ? "True" : match === "false" ? "False" : "None";
        },
    );
};

export const compactValue = (text) => {
    if (!text) return text;
    let out = "";
    let quote = null;
    let depth = 0;
    for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        if (quote) {
            out += ch;
            if (ch === quote && text[i - 1] !== "\\") quote = null;
            continue;
        }
        if (ch === '"' || ch === "'") {
            quote = ch;
            out += ch;
            continue;
        }
        if (ch === "(" || ch === "[" || ch === "{") depth++;
        else if (ch === ")" || ch === "]" || ch === "}") depth = Math.max(0, depth - 1);
        if (ch === " " && depth > 0 && out[out.length - 1] === ",") continue;
        out += ch;
    }
    return out;
};

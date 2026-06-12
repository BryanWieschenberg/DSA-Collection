import problemsData from "../../problems.json";

export const getTodayNY = () => {
    const options = {
        timeZone: "America/New_York",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    };
    const formatter = new Intl.DateTimeFormat("en-US", options);
    const parts = formatter.formatToParts(new Date());
    const year = parts.find((p) => p.type === "year").value;
    const month = parts.find((p) => p.type === "month").value;
    const day = parts.find((p) => p.type === "day").value;
    return `${year}-${month}-${day}`;
};

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
    return problemsData.find((p) => p.id === id) || null;
};

export const allProblems = problemsData;

export const DEFAULT_TIME_LIMIT_MS = 1000;
export const DEFAULT_MEMORY_LIMIT_MB = 128;

export const getLimits = (problem) => ({
    timeLimitMs: problem.timeLimit ?? DEFAULT_TIME_LIMIT_MS,
    memLimitMb: problem.memoryLimit ?? DEFAULT_MEMORY_LIMIT_MB,
});

export const getHiddenTests = (problem) =>
    Array.isArray(problem.hiddenTests) ? problem.hiddenTests : [];

export const pythonize = (text) => {
    if (!text) return text;
    const processed = text.replace(/\\?["']([TLQIG]\[.*?\])\\?["']/g, "$1");
    return processed.replace(
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

export const depythonize = (str) => {
    if (!str) return str;
    const processed = str.replace(
        /"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:True|False|None)\b/g,
        (match) => {
            if (match[0] === '"' || match[0] === "'") return match;
            return match === "True"
                ? "true"
                : match === "False"
                  ? "false"
                  : match === "None"
                    ? "null"
                    : match;
        },
    );
    return processed.replace(/([TLQIG]\[.*?\])/g, '"$1"');
};

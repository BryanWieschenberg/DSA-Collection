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

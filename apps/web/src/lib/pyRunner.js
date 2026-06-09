export function preloadPyodide() {
    return Promise.resolve();
}

export async function driver({
    userCode,
    functionName,
    isClass,
    cases,
    timeLimitMs = 3000,
    memLimitMb = 256,
    isSubmit = false,
    problemId = null,
}) {
    const finalize = (i, r) => {
        const isHidden = i >= cases.length;
        const c = isHidden ? null : cases[i];

        if (isHidden) {
            const showDetails = r.status === "RE" || r.status === "WA";
            return {
                ...r,
                hidden: !showDetails,
                label: `Test ${i + 1}`,
                input: showDetails ? (r.input ?? null) : null,
                expected: showDetails ? (r.expected ?? null) : null,
                output: showDetails ? (r.output ?? null) : null,
                stdout: showDetails ? (r.stdout ?? "") : "",
                error: r.error ?? null,
            };
        }
        return {
            ...r,
            hidden: false,
            label: `Case ${i + 1}`,
            input: c.input,
            expected: c.expected,
        };
    };

    let finalUserCode = userCode;
    if (!isClass && functionName) {
        const regex = new RegExp(`(def\\s+${functionName}\\s*\\()(\\s*self\\s*,)?`);
        finalUserCode = userCode.replace(regex, (match, defPart, selfPart) => {
            return selfPart ? match : `${defPart}self, `;
        });
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                userCode: finalUserCode,
                functionName,
                isClass,
                cases: cases.map((c) => ({
                    input: c.input,
                    expected: c.expected,
                    hidden: !!c.hidden,
                })),
                timeLimitMs,
                memLimitMb,
                isSubmit,
                problemId,
            }),
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const backendResults = await response.json();
        return backendResults.map((r, i) => finalize(i, r));
    } catch (err) {
        return cases.map((_, i) =>
            finalize(i, {
                status: "RE",
                error: `Failed to execute code on local backend. Make sure the server is running (e.g., via "pnpm dev" at the workspace root or "uvicorn app.main:app" inside apps/api) on port 8000.\n\nError details: ${err.message}`,
                stdout: "",
                output: null,
                timeMs: 0,
                memMb: 0,
            }),
        );
    }
}

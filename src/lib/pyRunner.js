const HANG_BUFFER_MS = 200;

let worker = null;
let readyPromise = null;

function spawnWorker() {
    worker = new Worker(new URL("./pyWorker.js", import.meta.url), { type: "module" });
    readyPromise = new Promise((resolve, reject) => {
        const onMsg = (e) => {
            if (e.data.type === "ready") {
                worker.removeEventListener("message", onMsg);
                resolve();
            } else if (e.data.type === "initError") {
                worker.removeEventListener("message", onMsg);
                reject(new Error(e.data.error));
            }
        };
        worker.addEventListener("message", onMsg);
    });
    worker.postMessage({ type: "init" });
    return readyPromise;
}

export function preloadPyodide() {
    if (!worker) return spawnWorker();
    return readyPromise;
}

function prime(src) {
    return new Promise((resolve) => {
        const onMsg = (e) => {
            if (e.data.type === "primed") {
                worker.removeEventListener("message", onMsg);
                resolve(e.data.compileError || null);
            }
        };
        worker.addEventListener("message", onMsg);
        worker.postMessage({ type: "prime", src });
    });
}

function runOneCase({ caseObj, fnName, isClass, timeLimitMs, memLimitMb }) {
    return new Promise((resolve, reject) => {
        const watchdog = setTimeout(() => {
            worker.removeEventListener("message", onMsg);
            reject({ hang: true });
        }, timeLimitMs + HANG_BUFFER_MS);

        const onMsg = (e) => {
            if (e.data.type === "result") {
                clearTimeout(watchdog);
                worker.removeEventListener("message", onMsg);
                resolve(e.data.result);
            }
        };
        worker.addEventListener("message", onMsg);
        worker.postMessage({
            type: "case",
            fnName,
            isClass,
            input: caseObj.input,
            expected: caseObj.expected,
            timeLimitMs,
            memLimitMb,
        });
    });
}

export async function driver({
    userCode,
    functionName,
    isClass,
    cases,
    timeLimitMs = 3000,
    memLimitMb = 256,
}) {
    let visibleCount = 0;
    let hiddenCount = 0;
    const meta = cases.map((c) =>
        c.hidden
            ? { hidden: true, label: `Hidden ${++hiddenCount}` }
            : { hidden: false, label: `Case ${++visibleCount}` },
    );

    const finalize = (i, r) => {
        const c = cases[i];
        const { hidden, label } = meta[i];
        if (hidden) {
            return {
                ...r,
                caseNum: i + 1,
                hidden: true,
                label,
                input: null,
                expected: null,
                output: null,
                stdout: "",
                error: r.status === "RE" ? "Error in hidden test." : (r.error ?? null),
            };
        }
        return { ...r, caseNum: i + 1, hidden: false, label, input: c.input, expected: c.expected };
    };

    try {
        await preloadPyodide();
    } catch {
        return cases.map((_, i) =>
            finalize(i, {
                status: "RE",
                error: "Failed to load the Python runtime. Check your network connection.",
                stdout: "",
                output: null,
            }),
        );
    }

    const compileError = await prime(userCode);
    if (compileError) {
        return cases.map((_, i) =>
            finalize(i, { status: "RE", error: compileError, stdout: "", output: null }),
        );
    }

    const results = [];
    for (let i = 0; i < cases.length; i++) {
        const c = cases[i];
        try {
            const r = await runOneCase({
                caseObj: c,
                fnName: functionName,
                isClass,
                timeLimitMs,
                memLimitMb,
            });
            results.push(finalize(i, r));
            if (r.status === "TLE" || r.status === "MLE") break;
        } catch {
            worker.terminate();
            worker = null;
            results.push(
                finalize(i, {
                    status: "TLE",
                    error: "Time Limit Exceeded",
                    stdout: "",
                    output: null,
                }),
            );
            break;
        }
    }
    return results;
}

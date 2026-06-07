import { useEffect, useState, useRef } from "react";

const MESSAGES = [
    "you'll be unemployed forever",
    "you're so dumb omg",
    "bruh",
    "skill issue",
    "L + ratio",
    "did you even read the problem?",
    "my grandma codes better",
    "have you considered a career change?",
    "404: brain not found",
    "Stack Overflow can't save you now",
    "git commit -m 'i give up'",
    "this is why we can't have nice things",
    "embarrassing, truly",
    "back to tutorials with you",
    "the compiler is laughing at you",
];

export default function FailureAnimation({ onDone }) {
    const [msg] = useState(() => MESSAGES[Math.floor(Math.random() * MESSAGES.length)]);
    const [exiting, setExiting] = useState(false);

    const onDoneRef = useRef(onDone);
    useEffect(() => {
        onDoneRef.current = onDone;
    }, [onDone]);

    useEffect(() => {
        const t1 = setTimeout(() => setExiting(true), 1100);
        const t2 = setTimeout(() => {
            if (onDoneRef.current) onDoneRef.current();
        }, 1500);
        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, []);

    return (
        <div
            className={`fixed inset-0 z-50 flex items-center justify-center bg-zinc-950/40 backdrop-blur-[1.5px] pointer-events-none ${exiting ? "animate-fade-out" : "animate-fade-in"}`}
        >
            <div className="flex flex-col items-center gap-4 animate-pop-in">
                <div
                    className="w-28 h-28 rounded-full bg-rose-500/15 border-4 border-rose-400 flex items-center justify-center shadow-2xl shadow-rose-500/30 animate-shake"
                    style={{ animationDelay: "0.35s" }}
                >
                    <svg
                        className="w-14 h-14 text-rose-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={3}
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                    </svg>
                </div>
                <div className="text-3xl font-bold text-rose-400">Rejected</div>
                <div className="text-base text-zinc-200 font-semibold">{msg}</div>
            </div>
        </div>
    );
}

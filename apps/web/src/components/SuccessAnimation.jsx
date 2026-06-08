import { useEffect, useState, useRef } from "react";

const COLORS = ["#34d399", "#60a5fa", "#fbbf24", "#f472b6", "#a78bfa", "#f87171"];

export default function SuccessAnimation({ onDone }) {
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

    const [confetti] = useState(() =>
        Array.from({ length: 50 }, (_, i) => ({
            left: Math.random() * 100,
            delay: Math.random() * 0.5,
            duration: 1 + Math.random() * 1,
            color: COLORS[i % COLORS.length],
            size: 6 + Math.random() * 8,
        })),
    );

    return (
        <div
            className={`fixed inset-0 z-50 flex items-center justify-center bg-zinc-950/40 backdrop-blur-[1.5px] pointer-events-none ${exiting ? "animate-fade-out" : "animate-fade-in"}`}
        >
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {confetti.map((c, i) => (
                    <span
                        key={i}
                        className="absolute rounded-sm"
                        style={{
                            left: `${c.left}%`,
                            top: "-30px",
                            width: c.size,
                            height: c.size,
                            background: c.color,
                            animation: `anim-confetti-fall ${c.duration}s ${c.delay}s ease-in forwards`,
                        }}
                    />
                ))}
            </div>

            <div className="flex flex-col items-center gap-4 animate-pop-in">
                <div className="w-28 h-28 rounded-full bg-emerald-500/15 border-4 border-emerald-400 flex items-center justify-center shadow-2xl shadow-emerald-500/30">
                    <svg
                        className="w-14 h-14 text-emerald-400"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={3}
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m4.5 12.75 6 6 9-13.5"
                        />
                    </svg>
                </div>
                <div className="text-3xl font-bold text-emerald-400">Accepted!</div>
            </div>
        </div>
    );
}

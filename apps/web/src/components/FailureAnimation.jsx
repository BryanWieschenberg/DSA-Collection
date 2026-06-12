import { useEffect, useState, useRef } from "react";

const MESSAGES = [
    "YOU'LL BE UNEMPLOYED FOREVER",
    "have u considered not be dumb?",
    "dude, just give up ur wasting ur time",
    "ur coworkers miss u... oh wait, u don't have any",
    "that ain't it chief just give up",
    "don't worry, somewhere out there a hiring manager's about to ghost u",
    "have u considered a career change?",
    "CAPTCHA asks u to prove ur not a bot out of pity, not suspicion",
    "embarrassing, genuinely",
    "u should be ashamed of urself",
    "the only thing emptier than ur prospects is ur bank account",
    "a rejection email would actually be exciting at this point",
    "ur parents have stopped asking, which is somehow worse",
    "0 new notifications",
    "yeah keep on manifesting (it's not working)",
    "you've already been replaced by AI",
    "birds are chirping, flowers are blooming, capitalism keeps moving",
    "everyone likes an underdog, but ur not even in the race",
    "i don't think i've ever met anyone as lazy and pathetic as u, i know dogs who are better workers than u, DOGS. at least they actually contribute valuable services to the world. what do u do? sit on ur computer solving silly little logic puzzles? get a grip. its time to wake up",
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
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M6 18 18 6M6 6l12 12"
                        />
                    </svg>
                </div>
                <div className="text-3xl font-bold text-rose-400">Rejected</div>
                <div className="text-base text-zinc-200 font-semibold">{msg}</div>
            </div>
        </div>
    );
}

import { useEffect, useState, useRef, useCallback } from "react";

interface SuccessAnimationProps {
  show: boolean;
  onComplete: () => void;
}

export default function SuccessAnimation({ show, onComplete }: SuccessAnimationProps) {
  const [phase, setPhase] = useState<"idle" | "enter" | "hold" | "fadeout">("idle");
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stableOnComplete = useCallback(onComplete, [onComplete]);

  useEffect(() => {
    if (show) {
      setPhase("enter");

      timerRef.current = setTimeout(() => setPhase("hold"), 250);
      const t2 = setTimeout(() => setPhase("fadeout"), 1200);
      const t3 = setTimeout(() => {
        setPhase("idle");
        stableOnComplete();
      }, 1700);

      return () => {
        if (timerRef.current) clearTimeout(timerRef.current);
        clearTimeout(t2);
        clearTimeout(t3);
      };
    }
  }, [show, stableOnComplete]);

  if (phase === "idle") return null;

  return (
    <div
      className="fixed inset-0 z-50 pointer-events-none flex items-center justify-center"
      style={{
        opacity: phase === "fadeout" ? 0 : 1,
        transition: "opacity 0.5s ease-out",
      }}
    >
      {/* Light backdrop */}
      <div
        className="absolute inset-0 bg-surface-900/30"
        style={{
          opacity: phase === "enter" || phase === "hold" ? 1 : 0,
          transition: "opacity 0.25s ease",
        }}
      />

      {/* Expanding ring */}
      <div
        className="absolute rounded-full border border-green/25"
        style={{
          width: phase !== "enter" ? "300px" : "0px",
          height: phase !== "enter" ? "300px" : "0px",
          opacity: phase === "hold" ? 0.2 : 0.5,
          transition: "all 0.5s cubic-bezier(0.22, 1, 0.36, 1)",
        }}
      />

      {/* Center badge */}
      <div
        className="relative flex flex-col items-center gap-3"
        style={{
          transform: phase === "enter" ? "scale(0.6)" : "scale(1)",
          opacity: phase === "enter" ? 0 : 1,
          transition: "all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
        }}
      >
        {/* Glowing checkmark circle */}
        <div
          className="relative w-16 h-16 rounded-full flex items-center justify-center"
          style={{
            background: "linear-gradient(135deg, #4ade80, #22c55e)",
            boxShadow: phase === "hold"
              ? "0 0 40px rgba(74, 222, 128, 0.5), 0 0 80px rgba(74, 222, 128, 0.15)"
              : "0 0 15px rgba(74, 222, 128, 0.3)",
            transition: "box-shadow 0.3s ease",
          }}
        >
          <svg
            className="w-8 h-8 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={3}
            style={{
              strokeDasharray: 30,
              strokeDashoffset: phase === "hold" ? 0 : 30,
              transition: "stroke-dashoffset 0.25s ease 0.1s",
            }}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>

        {/* Text */}
        <div className="text-center">
          <h2
            className="text-xl font-bold text-text-primary tracking-tight"
            style={{
              opacity: phase === "hold" ? 1 : 0,
              transform: phase === "hold" ? "translateY(0)" : "translateY(6px)",
              transition: "all 0.25s ease 0.15s",
            }}
          >
            All Tests Passed!
          </h2>
        </div>
      </div>
    </div>
  );
}

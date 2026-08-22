const STAGES = [
  { key: "flight", label: "Flight" },
  { key: "hotel", label: "Hotel" },
  { key: "itinerary", label: "Itinerary" },
  { key: "final", label: "Response" },
];

export default function ProgressPath({ active }) {
  return (
    <div className="mt-10 mb-2" aria-live="polite">
      <p className="text-[11px] font-mono uppercase tracking-wider text-parchment-muted mb-6 text-center">
        {active ? "Agents in flight…" : "Route complete"}
      </p>

      <div className="relative">
        {/* base line */}
        <div className="absolute top-[7px] left-[12.5%] right-[12.5%] h-px bg-dusk-line" />

        {/* travelling dot, only while active */}
        {active && (
          <div className="absolute top-[3px] left-[12.5%] right-[12.5%] h-[15px] pointer-events-none">
            <div className="relative w-full h-full">
              <div className="travel-dot absolute w-[9px] h-[9px] rounded-full bg-amber shadow-[0_0_10px_2px_rgba(232,163,61,0.6)]" />
            </div>
          </div>
        )}

        <div className="relative z-10 flex justify-between">
          {STAGES.map((s) => (
            <div key={s.key} className="flex flex-col items-center gap-3 w-1/4">
              <div
                className={`w-3.5 h-3.5 rounded-full border-2 border-amber transition-colors duration-500 ${
                  active ? "bg-dusk" : "bg-amber"
                }`}
              />
              <span className="text-[11px] font-mono uppercase tracking-wider text-parchment-muted text-center">
                {s.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

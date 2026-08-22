import { useState } from "react";
import TripForm from "./components/TripForm";
import ProgressPath from "./components/ProgressPath";
import ResultsView from "./components/ResultsView";
import { planTrip } from "./api";

export default function App() {
  const [status, setStatus] = useState("idle"); // idle | loading | done | error
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(payload) {
    setStatus("loading");
    setError("");
    setResult(null);
    try {
      const data = await planTrip(payload);
      setResult(data);
      setStatus("done");
    } catch (err) {
      setError(err.message || "Something went wrong.");
      setStatus("error");
    }
  }

  return (
    <div className="min-h-screen bg-dusk">
      <div className="max-w-3xl mx-auto px-5 sm:px-8 py-14 sm:py-20">
        <header className="mb-12">
          <div className="text-xs font-mono uppercase tracking-[0.25em] text-lagoon mb-3">
            Voyagent
          </div>
          <h1 className="font-display font-medium text-4xl sm:text-5xl leading-[1.1] text-parchment">
            Plan the trip.
            <br />
            <span className="text-amber italic">Skip the fifty tabs.</span>
          </h1>
          <p className="mt-4 text-parchment-muted max-w-lg leading-relaxed">
            Four agents split the work &mdash; flights, stays, things to do
            &mdash; and hand it all to one final pass that writes your plan.
          </p>
        </header>

        <TripForm onSubmit={handleSubmit} loading={status === "loading"} />

        {(status === "loading" || status === "done") && (
          <ProgressPath active={status === "loading"} />
        )}

        {status === "error" && (
          <div
            role="alert"
            className="mt-8 border border-red-900/50 bg-red-950/30 text-red-200 rounded-xl px-5 py-4"
          >
            <p className="font-medium">Couldn&apos;t plan this trip.</p>
            <p className="text-sm text-red-300/80 mt-1">{error}</p>
          </div>
        )}

        {status === "done" && result && <ResultsView result={result} />}

        <footer className="mt-20 text-[11px] text-parchment-muted/50 font-mono tracking-wide">
          Flight &middot; Hotel &middot; Itinerary &middot; Final Response &mdash; one shared
          state, four agents.
        </footer>
      </div>
    </div>
  );
}

import { useState } from "react";

const initialForm = {
  origin: "",
  destination: "",
  departure_date: "",
  return_date: "",
  adults: 1,
  budget: "",
  trip_length_days: "",
  interests: "",
};

export default function TripForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialForm);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({
      ...form,
      adults: Number(form.adults) || 1,
      interests: form.interests
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
      return_date: form.return_date || null,
      budget: form.budget || null,
      trip_length_days: form.trip_length_days || null,
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="relative bg-dusk-card border border-dusk-line rounded-2xl p-6 sm:p-8 shadow-2xl shadow-black/30"
    >
      <div className="absolute -top-3 left-7 bg-amber text-dusk-deep text-[11px] font-mono tracking-[0.2em] uppercase px-3 py-1 rounded-full">
        Boarding pass
      </div>

      <div className="grid sm:grid-cols-2 gap-5 mt-2">
        <Field label="From" required>
          <input
            required
            value={form.origin}
            onChange={(e) => update("origin", e.target.value)}
            placeholder="Islamabad"
            className="input"
          />
        </Field>

        <Field label="To" required>
          <input
            required
            value={form.destination}
            onChange={(e) => update("destination", e.target.value)}
            placeholder="Budapest"
            className="input"
          />
        </Field>

        <Field label="Depart" required>
          <input
            required
            type="date"
            value={form.departure_date}
            onChange={(e) => update("departure_date", e.target.value)}
            className="input"
          />
        </Field>

        <Field label="Return (optional)">
          <input
            type="date"
            value={form.return_date}
            onChange={(e) => update("return_date", e.target.value)}
            className="input"
          />
        </Field>

        <Field label="Travellers">
          <input
            type="number"
            min="1"
            value={form.adults}
            onChange={(e) => update("adults", e.target.value)}
            className="input"
          />
        </Field>

        <Field label="Budget in USD (optional)">
          <input
            value={form.budget}
            onChange={(e) => update("budget", e.target.value)}
            placeholder="5000"
            className="input"
          />
        </Field>

        <Field label="Trip length in days (optional)">
          <input
            value={form.trip_length_days}
            onChange={(e) => update("trip_length_days", e.target.value)}
            placeholder="7"
            className="input"
          />
        </Field>

        <Field label="Interests (optional)">
          <input
            value={form.interests}
            onChange={(e) => update("interests", e.target.value)}
            placeholder="nature, food, history"
            className="input"
          />
        </Field>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="mt-7 w-full sm:w-auto inline-flex items-center justify-center gap-2
          bg-amber hover:bg-amber-soft disabled:opacity-50 disabled:cursor-not-allowed
          text-dusk-deep font-semibold px-7 py-3 rounded-full transition-colors
          focus:outline-none focus-visible:ring-2 focus-visible:ring-amber focus-visible:ring-offset-2 focus-visible:ring-offset-dusk-card"
      >
        {loading ? "Charting your route…" : "Plan my trip"}
      </button>
    </form>
  );
}

function Field({ label, required, children }) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-[11px] font-mono uppercase tracking-wider text-parchment-muted">
        {label} {required && <span className="text-amber">*</span>}
      </span>
      {children}
    </label>
  );
}

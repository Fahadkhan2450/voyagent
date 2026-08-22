import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ResultsView({ result }) {
  return (
    <div className="mt-10 space-y-6">
      <div className="bg-dusk-card border border-dusk-line rounded-2xl p-6 sm:p-8">
        <h2 className="font-display text-2xl sm:text-3xl text-amber mb-5">
          Your itinerary
        </h2>
        <div
          className="prose prose-invert max-w-none
            prose-headings:font-display prose-headings:text-parchment prose-headings:mt-8 prose-headings:mb-3
            prose-h1:text-2xl prose-h2:text-xl prose-h3:text-base prose-h3:uppercase prose-h3:tracking-wide prose-h3:text-lagoon prose-h3:font-body prose-h3:font-semibold
            prose-p:text-parchment/90 prose-p:leading-relaxed
            prose-strong:text-amber prose-strong:font-semibold
            prose-li:text-parchment/90 prose-li:my-1
            prose-a:text-lagoon prose-a:no-underline hover:prose-a:underline
            prose-hr:border-dusk-line prose-hr:my-8
            prose-table:my-0"
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              // wrap tables in a horizontally-scrollable, styled container
              // so wide pricing/itinerary tables don't break mobile layout
              table: ({ children }) => (
                <div className="not-prose my-6 overflow-x-auto rounded-lg border border-dusk-line">
                  <table className="w-full text-sm border-collapse">
                    {children}
                  </table>
                </div>
              ),
              thead: ({ children }) => (
                <thead className="bg-dusk-deep/80 sticky top-0">{children}</thead>
              ),
              th: ({ children }) => (
                <th className="text-left font-mono text-[11px] uppercase tracking-wider text-amber px-4 py-3 whitespace-nowrap border-b border-dusk-line">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="px-4 py-3 text-parchment/90 align-top border-b border-dusk-line/60">
                  {children}
                </td>
              ),
              tr: ({ children }) => (
                <tr className="even:bg-dusk-deep/30">{children}</tr>
              ),
            }}
          >
            {result.final_response}
          </ReactMarkdown>
        </div>
      </div>

      <RawSection title="Flight search results" items={result.flight_results} />
      <RawSection title="Hotel search results" items={result.hotel_results} />
      <RawSection
        title="Activities &amp; points of interest"
        items={result.itinerary}
      />
    </div>
  );
}

function RawSection({ title, items }) {
  const [open, setOpen] = useState(false);
  if (!items || items.length === 0) return null;

  return (
    <div className="border border-dusk-line rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-5 py-3.5 bg-dusk-card/60 hover:bg-dusk-card transition-colors text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-amber/60"
        aria-expanded={open}
      >
        <span className="font-mono text-xs uppercase tracking-wider text-parchment-muted">
          {title} ({items.length})
        </span>
        <span className="text-amber text-lg leading-none">{open ? "\u2212" : "+"}</span>
      </button>
      {open && (
        <ul className="divide-y divide-dusk-line">
          {items.map((item, i) => (
            <li key={i} className="px-5 py-4">
              {item.url ? (
                <a
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-lagoon hover:underline font-medium"
                >
                  {item.title || item.url}
                </a>
              ) : (
                <span className="font-medium text-parchment">{item.title}</span>
              )}
              {item.snippet && (
                <p className="text-sm text-parchment-muted mt-1">{item.snippet}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

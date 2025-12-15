export default function MemoryIndicator({ trace }) {
  if (!trace?.some(t => t.includes("semantic recall"))) return null;

  return (
    <div className="card" style={{ borderLeft: "6px solid var(--memory)" }}>
      🧠 <strong>Semantic Memory Used</strong>
      <p style={{ color: "var(--muted)" }}>
        Parallax reused prior knowledge to avoid redundant computation.
      </p>
    </div>
  );
}

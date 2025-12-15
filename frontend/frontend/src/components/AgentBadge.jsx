export default function AgentBadge({ agents, confidence }) {
  if (!agents) return null;

  return (
    <div className="card">
      <div className="badges">
        {agents.map((a) => (
          <span
            key={a}
            className={`badge ${a.toLowerCase().replace("agent", "")}`}
          >
            {a}
          </span>
        ))}
        <span style={{ marginLeft: "auto", color: "var(--muted)" }}>
          Confidence: {Math.round(confidence * 100)}%
        </span>
      </div>
    </div>
  );
}

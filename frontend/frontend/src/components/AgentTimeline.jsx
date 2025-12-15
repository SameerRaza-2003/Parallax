export default function AgentTimeline({ agents }) {
  if (!agents?.length) return null;

  return (
    <div className="card">
      <h3>Agent Execution Timeline</h3>
      <div style={{ display: "flex", gap: "1rem" }}>
        {agents.map((agent, i) => (
          <div
            key={agent}
            style={{
              padding: "0.6rem 1rem",
              borderRadius: "999px",
              background:
                agent === "MemoryAgent"
                  ? "var(--memory)"
                  : agent === "ResearchAgent"
                  ? "var(--research)"
                  : "var(--analysis)",
              color: "white",
              animation: `fadeIn 0.5s ease ${i * 0.2}s both`,
            }}
          >
            {agent}
          </div>
        ))}
      </div>
    </div>
  );
}

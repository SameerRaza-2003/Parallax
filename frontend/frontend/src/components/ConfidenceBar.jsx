export default function ConfidenceBar({ value }) {
  if (value == null) return null;

  return (
    <div className="card">
      <h3>Model Confidence</h3>
      <div
        style={{
          background: "#e5e7eb",
          borderRadius: "999px",
          height: "12px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${value * 100}%`,
            background: value > 0.7 ? "var(--memory)" : "#f59e0b",
            height: "100%",
            transition: "width 0.6s ease",
          }}
        />
      </div>
      <small>{Math.round(value * 100)}%</small>
    </div>
  );
}

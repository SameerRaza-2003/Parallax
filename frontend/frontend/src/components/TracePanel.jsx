export default function TracePanel({ trace }) {
  if (!trace?.length) return null;

  return (
    <div className="card">
      <h3>Reasoning Trace</h3>
      <ul className="trace">
        {trace.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>
    </div>
  );
}

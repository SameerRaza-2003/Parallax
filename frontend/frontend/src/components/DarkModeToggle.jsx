export default function DarkModeToggle({ dark, setDark }) {
  return (
    <button
      onClick={() => setDark(!dark)}
      style={{
        marginLeft: "auto",
        background: "transparent",
        color: "var(--text)",
        border: "1px solid var(--muted)",
      }}
    >
      {dark ? "☀ Light" : "🌙 Dark"}
    </button>
  );
}

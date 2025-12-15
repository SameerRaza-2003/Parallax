import { useState } from "react";

export default function QueryBox({ onSubmit, loading }) {
  const [question, setQuestion] = useState("");

  return (
    <div className="card">
      <textarea
        placeholder="Ask Parallax a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={() => onSubmit(question)} disabled={loading}>
        {loading ? "Reasoning..." : "Ask Parallax"}
      </button>
    </div>
  );
}

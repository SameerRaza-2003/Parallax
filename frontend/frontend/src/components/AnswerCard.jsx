import TypingText from "./TypingText";

export default function AnswerCard({ answer, animate }) {
  if (!answer) return null;

  return (
    <div className="card">
      <h3>Final Answer</h3>
      {animate ? (
        <TypingText text={answer} />
      ) : (
        <p style={{ whiteSpace: "pre-line" }}>{answer}</p>
      )}
    </div>
  );
}

import { useEffect, useState } from "react";

export default function TypingText({ text, speed = 15 }) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed("");
    let i = 0;
    const interval = setInterval(() => {
      setDisplayed((prev) => prev + text[i]);
      i++;
      if (i >= text.length) clearInterval(interval);
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed]);

  return <p style={{ whiteSpace: "pre-line" }}>{displayed}</p>;
}

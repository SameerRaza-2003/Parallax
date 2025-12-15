import { useEffect, useState } from "react";
import { askQuestion } from "./services/api";

import QueryBox from "./components/QueryBox";
import TracePanel from "./components/TracePanel";
import AgentBadge from "./components/AgentBadge";
import AgentTimeline from "./components/AgentTimeline";
import MemoryIndicator from "./components/MemoryIndicator";
import ConfidenceBar from "./components/ConfidenceBar";
import DarkModeToggle from "./components/DarkModeToggle";
import TypingText from "./components/TypingText";

import "./index.css";

/**
 * PARALLAX
 * Multi-Agent Intelligent Reasoning Platform
 * ------------------------------------------
 * Dashboard-style conversational AI with
 * semantic memory and transparent agent orchestration.
 */

export default function App() {
  /* ================= UI STATE ================= */
  const [dark, setDark] = useState(false);
  const [loading, setLoading] = useState(false);
  const [animateAnswer, setAnimateAnswer] = useState(false);

  /* ================= SESSION STATE ================= */
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);

  /* ================= THEME ================= */
  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      dark ? "dark" : "light"
    );
  }, [dark]);

  /* ================= DERIVED DATA ================= */
  const activeSession = sessions.find(
    (s) => s.id === activeSessionId
  );

  const lastAssistantMessage =
    activeSession?.messages
      ?.filter((m) => m.role === "assistant")
      ?.slice(-1)[0]?.content;

  /* ================= SESSION CONTROL ================= */

  const startNewSession = () => {
    // Prevent multiple empty conversations (ChatGPT-style)
    if (activeSession && activeSession.messages.length === 0) return;

    const id = `session-${Date.now()}`;
    const newSession = {
      id,
      title: "New conversation",
      messages: [],
      meta: null,
    };

    setSessions((prev) => [newSession, ...prev]);
    setActiveSessionId(id);
    setAnimateAnswer(false);
  };

  const selectSession = (id) => {
    setActiveSessionId(id);
    setAnimateAnswer(false);
  };

  /* ================= QUERY HANDLER ================= */

  const handleAsk = async (question) => {
    if (!question) return;

    let sessionId = activeSessionId;

    // Create first session only once
    if (!sessionId) {
      const id = `session-${Date.now()}`;
      const newSession = {
        id,
        title: question.slice(0, 40) + "...",
        messages: [],
        meta: null,
      };

      setSessions((prev) => [newSession, ...prev]);
      setActiveSessionId(id);
      sessionId = id;
    }

    setLoading(true);
    setAnimateAnswer(true);

    try {
      const res = await askQuestion(question);

      setSessions((prev) =>
        prev.map((s) =>
          s.id === sessionId
            ? {
                ...s,
                title:
                  s.title === "New conversation"
                    ? question.slice(0, 40) + "..."
                    : s.title,
                messages: [
                  ...s.messages,
                  { role: "user", content: question },
                  { role: "assistant", content: res.final_answer },
                ],
                meta: res,
              }
            : s
        )
      );
    } catch (err) {
      console.error(err);
      alert("Backend error — ensure FastAPI is running");
    } finally {
      setLoading(false);
    }
  };

  /* ================= RENDER ================= */

  return (
    <div className="dashboard">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <h2>Parallax</h2>
        <p style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
          Multi-Agent Reasoning Platform
        </p>

        <button
          onClick={startNewSession}
          style={{ width: "100%", marginBottom: "1rem" }}
        >
          + New Conversation
        </button>

        {sessions.map((s) => {
          const preview =
            s.messages.find((m) => m.role === "user")?.content ||
            s.title;

          return (
            <div
              key={s.id}
              onClick={() => selectSession(s.id)}
              style={{
                padding: "0.6rem 0.7rem",
                borderRadius: "8px",
                cursor: "pointer",
                background:
                  s.id === activeSessionId
                    ? "var(--bg)"
                    : "transparent",
                marginBottom: "0.4rem",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {preview}
            </div>
          );
        })}
      </aside>

      {/* MAIN PANEL */}
      <main className="main">
        <div className="header">
          <h1>Interactive Reasoning Console</h1>
          <DarkModeToggle dark={dark} setDark={setDark} />
        </div>

        <p style={{ color: "var(--muted)", maxWidth: "720px" }}>
          Parallax orchestrates specialized AI agents, reuses semantic
          memory, and exposes the full reasoning pipeline through a
          transparent, dashboard-style interface.
        </p>

        <div className="chat-input">
          <QueryBox onSubmit={handleAsk} loading={loading} />
        </div>

        {activeSession?.meta && (
          <>
            <MemoryIndicator trace={activeSession.meta.trace} />

            <div className="card">
              <h3>Final Answer</h3>
              {animateAnswer ? (
                <TypingText text={lastAssistantMessage || ""} />
              ) : (
                <p style={{ whiteSpace: "pre-line" }}>
                  {lastAssistantMessage}
                </p>
              )}
            </div>

            <AgentTimeline
              agents={activeSession.meta.agents_used}
            />

            <TracePanel trace={activeSession.meta.trace} />

            <AgentBadge
              agents={activeSession.meta.agents_used}
              confidence={activeSession.meta.confidence}
            />

            <ConfidenceBar value={activeSession.meta.confidence} />
          </>
        )}
      </main>
    </div>
  );
}

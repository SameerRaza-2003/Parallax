import json
from app.core.llm_client import LLMClient
from app.agents.research import ResearchAgent
from app.agents.analysis import AnalysisAgent
from app.agents.memory import MemoryAgent
from app.utils.output_writer import OutputWriter


class Coordinator:
    """
    Coordinator (Manager) Agent

    Responsibilities:
    - LLM-based task planning
    - Semantic memory reuse to avoid redundant work
    - Orchestration of Research, Analysis, and Memory agents
    - Traceable and robust execution
    - Automatic output logging (assignment requirement)
    """

    def __init__(self):
        self.llm = LLMClient()
        self.research_agent = ResearchAgent(self.llm)
        self.analysis_agent = AnalysisAgent(self.llm)
        self.memory_agent = MemoryAgent()
        self.output_writer = OutputWriter()

    # -------------------------------------------------
    # LLM-BASED PLANNING
    # -------------------------------------------------
    def plan(self, question: str):
        system_prompt = """
You are a Coordinator Agent in a multi-agent system.

Available agents:
- MemoryAgent
- ResearchAgent
- AnalysisAgent

Rules:
- Use MemoryAgent for past knowledge.
- Use ResearchAgent for new information.
- Use AnalysisAgent for reasoning or comparison.
- Use the minimum number of agents required.
Return ONLY a JSON list of agent names.
"""

        try:
            plan_text = self.llm.generate(system_prompt, question)
            return json.loads(plan_text)
        except Exception:
            # Safe fallback (mandatory robustness)
            return ["ResearchAgent", "AnalysisAgent"]

    # -------------------------------------------------
    # MAIN QUERY HANDLER
    # -------------------------------------------------
    def handle_query(self, question: str):
        trace = []
        agents_used = []
        context = {}

        # 🔁 STEP 1: SEMANTIC MEMORY CHECK
        try:
            recalled, score = self.memory_agent.recall(question)
            trace.append(
                f"MemoryAgent checked semantic memory (score={round(score, 2)})"
            )
        except Exception as e:
            recalled, score = None, 0.0
            trace.append(f"Memory recall failed: {str(e)}")

        if recalled:
            trace.append("MemoryAgent semantic recall triggered")
            trace.append("Redundant computation avoided")

            response = {
                "final_answer": recalled,
                "agents_used": ["MemoryAgent"],
                "trace": trace,
                "confidence": round(score, 2)
            }

            # 📝 SAVE OUTPUT
            self.output_writer.save("memory_test", {
                "question": question,
                **response
            })

            return response

        # 🧠 STEP 2: PLAN AGENTS
        plan = self.plan(question)
        trace.append(f"Coordinator planned agent sequence: {plan}")

        # ⚙️ STEP 3: EXECUTE PLAN
        for agent in plan:
            if agent == "ResearchAgent":
                trace.append("ResearchAgent invoked (LLM-based)")
                context["research"] = self.research_agent.run(question)
                agents_used.append("ResearchAgent")

            elif agent == "AnalysisAgent":
                trace.append("AnalysisAgent invoked (LLM-based)")
                context["analysis"] = self.analysis_agent.run(question, context)
                agents_used.append("AnalysisAgent")

            elif agent == "MemoryAgent":
                trace.append("MemoryAgent explicitly queried")
                context["memory"] = self.memory_agent.get_conversation_memory()
                agents_used.append("MemoryAgent")

        # 🧩 STEP 4: FINAL ANSWER
        final_answer = (
            context.get("analysis")
            or context.get("research")
            or "No response generated."
        )

        # 🧠 STEP 5: STORE MEMORY
        self.memory_agent.store_conversation(
            question=question,
            response=final_answer,
            agents=agents_used
        )

        response = {
            "final_answer": final_answer,
            "agents_used": agents_used,
            "trace": trace,
            "confidence": 0.9
        }

        # 📝 STEP 6: AUTO-SAVE OUTPUT (MANDATORY)
        q_lower = question.lower()
        if "compare" in q_lower:
            label = "collaborative"
        elif "analyze" in q_lower:
            label = "complex_query"
        elif "find" in q_lower or "research" in q_lower:
            label = "multi_step"
        else:
            label = "simple_query"

        self.output_writer.save(label, {
            "question": question,
            **response
        })

        return response

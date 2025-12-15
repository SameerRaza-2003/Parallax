class AnalysisAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, question: str, context: dict):
        system_prompt = """
You are an Analysis Agent.
Analyze the research provided.
Compare methods, highlight trade-offs,
and produce a clear conclusion.
"""

        research = context.get("research", "")

        user_prompt = f"""
User Question:
{question}

Research Findings:
{research}
"""

        return self.llm.generate(system_prompt, user_prompt)

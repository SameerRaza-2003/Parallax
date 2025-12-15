class ResearchAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, topic: str):
        system_prompt = """
You are a Research Agent in a multi-agent system.
Simulate searching reliable academic and technical sources.
Return concise bullet-point findings.
"""

        return self.llm.generate(system_prompt, topic)

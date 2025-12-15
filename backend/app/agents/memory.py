from datetime import datetime
from app.memory.vector_store import VectorStore


class MemoryAgent:
    """
    Memory Agent

    Responsibilities:
    - Store structured conversation history
    - Maintain semantic memory using vector embeddings
    - Recall past knowledge to avoid redundant computation
    """

    def __init__(self):
        self.conversation_memory = []
        self.vector_store = VectorStore()

    def store_conversation(self, question: str, response: str, agents: list):
        """
        Store conversation record and semantic embedding.
        Both question and answer are embedded together
        to maximize semantic recall accuracy.
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "agents": agents,
            "response": response
        }

        # Store structured history
        self.conversation_memory.append(record)

        # Store semantic memory (question + answer)
        combined_text = f"Question: {question}\nAnswer: {response}"

        try:
            self.vector_store.add(combined_text)
        except Exception:
            # Memory failure should NEVER crash the system
            pass

    def recall(self, query: str, threshold: float = 0.45):
        """
        Perform semantic recall using vector similarity.
        Returns recalled text and similarity score if above threshold.
        """
        try:
            text, score = self.vector_store.search(query)
        except Exception:
            return None, 0.0

        if text and score >= threshold:
            return text, score

        return None, score

    def get_conversation_memory(self):
        """
        Return full conversation history.
        """
        return self.conversation_memory

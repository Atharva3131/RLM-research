# src/core/llm.py
"""
LLM abstraction layer.
Keeps model providers decoupled from agent logic.
"""

from mistralai import Mistral


class MistralLLM:
    def __init__(
        self,
        api_key: str,
        model: str = "mistral-large-latest",
        temperature: float = 0.0,
    ):
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        """
        Unified invoke interface expected by all agents.
        """
        messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return response.choices[0].message.content
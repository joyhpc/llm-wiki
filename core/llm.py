from abc import ABC, abstractmethod
from anthropic import Anthropic
import ollama

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class OllamaProvider(LLMProvider):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

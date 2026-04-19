import pytest
from core.llm import LLMProvider, ClaudeProvider, OllamaProvider

def test_claude_provider_generate():
    provider = ClaudeProvider(api_key="test-key", model="claude-opus-4-6")
    result = provider.generate("Hello")
    assert isinstance(result, str)
    assert len(result) > 0

def test_ollama_provider_generate():
    provider = OllamaProvider(model="llama2")
    result = provider.generate("Hello")
    assert isinstance(result, str)
    assert len(result) > 0

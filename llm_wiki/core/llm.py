from abc import ABC, abstractmethod
from anthropic import Anthropic
import ollama
import os

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class ClaudeProvider(LLMProvider):
    def __init__(self, config: dict):
        """初始化 Claude Provider

        Args:
            config: llm 配置字典，包含 api_key 和 model
        """
        api_key = config.get('api_key', '')
        # 支持环境变量替换
        if api_key.startswith('${') and api_key.endswith('}'):
            env_var = api_key[2:-1]
            api_key = os.getenv(env_var, '')

        model = config.get('model', 'claude-sonnet-4-20250514')
        base_url = os.getenv('ANTHROPIC_BASE_URL')

        if base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        else:
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
    def __init__(self, config: dict):
        """初始化 Ollama Provider

        Args:
            config: llm 配置字典，包含 model
        """
        self.model = config.get('model', 'llama2')

    def generate(self, prompt: str) -> str:
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

class ClaudeCodeProvider(LLMProvider):
    """Claude Code 环境 Provider，复用当前会话"""

    def __init__(self):
        # Claude Code 环境下不需要 API key
        pass

    def generate(self, prompt: str) -> str:
        """使用当前 Claude Code 会话生成响应"""
        # 注意：这里假设在 Claude Code 环境中运行
        # 实际实现需要调用 Claude Code 的内部 API
        # 暂时抛出 NotImplementedError，等待实际集成
        raise NotImplementedError(
            "ClaudeCodeProvider requires Claude Code runtime integration"
        )

class CodexProvider(LLMProvider):
    """Codex 环境 Provider，复用当前会话"""

    def __init__(self):
        pass

    def generate(self, prompt: str) -> str:
        """使用当前 Codex 会话生成响应"""
        raise NotImplementedError(
            "CodexProvider requires Codex runtime integration"
        )

def create_llm_provider(config: dict) -> LLMProvider:
    """根据配置创建 LLM Provider

    Args:
        config: 配置字典，包含 llm 配置

    Returns:
        LLMProvider 实例
    """
    llm_config = config.get('llm', {})
    provider = llm_config.get('provider', 'auto')

    if provider == 'auto':
        # 检测 Claude Code 环境
        if os.getenv('CLAUDE_CODE_SESSION'):
            return ClaudeCodeProvider()
        # 检测 Codex 环境
        elif os.getenv('CODEX_SESSION'):
            return CodexProvider()
        # 回退到 Claude API
        else:
            return ClaudeProvider(llm_config)
    elif provider == 'claude':
        return ClaudeProvider(llm_config)
    elif provider == 'ollama':
        return OllamaProvider(llm_config)
    else:
        raise ValueError(f"Unknown provider: {provider}")


from pathlib import Path
from typing import Dict
from core.llm import LLMProvider
from core.search import search_wiki

def query_wiki(question: str, wiki_dir: Path, llm: LLMProvider) -> Dict[str, str]:
    """查询 wiki 并返回答案"""
    search_results = search_wiki(wiki_dir, question, max_results=5)

    if not search_results:
        return {
            'answer': 'No relevant information found in the wiki.',
            'sources': []
        }

    context_parts = []
    sources = set()
    for result in search_results:
        file_path = Path(result['file'])
        sources.add(file_path.name)
        content = file_path.read_text(encoding='utf-8')
        context_parts.append(f"From {file_path.name}:\n{content}\n")

    context = '\n---\n'.join(context_parts)

    prompt = f"""You are answering questions based on a wiki.

Question: {question}

Relevant wiki pages:
{context}

Provide a clear answer based on the information above. Cite the source pages.

Format:
Answer: <your answer>

Sources:
- <page1.md>
- <page2.md>
"""

    response = llm.generate(prompt)
    answer, cited_sources = _parse_query_response(response)

    return {
        'answer': answer,
        'sources': cited_sources if cited_sources else list(sources)
    }

def _parse_query_response(response: str) -> tuple[str, list]:
    """解析 LLM 查询响应"""
    lines = response.split('\n')
    answer_lines = []
    sources = []
    in_answer = False
    in_sources = False

    for line in lines:
        if line.startswith('Answer:'):
            in_answer = True
            answer_lines.append(line.replace('Answer:', '').strip())
        elif line.startswith('Sources:'):
            in_answer = False
            in_sources = True
        elif in_answer:
            answer_lines.append(line)
        elif in_sources and line.strip().startswith('-'):
            sources.append(line.strip().lstrip('- '))

    answer = '\n'.join(answer_lines).strip()
    return answer, sources

from core.router import detect_query_target

def query_wiki_auto(question: str, base_path: Path, llm: LLMProvider) -> Dict[str, str]:
    """自动检测目标并查询"""
    target = detect_query_target(question)
    wiki_dir = base_path / target
    return query_wiki(question, wiki_dir, llm)

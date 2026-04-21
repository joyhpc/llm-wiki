from pathlib import Path
from typing import List, Dict, Tuple
from llm_wiki.core.llm import LLMProvider
import re

def find_similar_pages(wiki_dir: Path, category: str, llm: LLMProvider, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    """查找语义相似的页面

    Args:
        wiki_dir: wiki 根目录
        category: 类别（concepts, entities）
        llm: LLM provider
        threshold: 相似度阈值（0-1）

    Returns:
        相似页面对列表 [(page1, page2, similarity), ...]
    """
    category_dir = wiki_dir / category
    if not category_dir.exists():
        return []

    pages = list(category_dir.glob('*.md'))
    if len(pages) < 2:
        return []

    # 提取页面标题
    page_titles = {}
    for page in pages:
        content = page.read_text(encoding='utf-8')
        # 提取第一行标题
        first_line = content.split('\n')[0]
        title = first_line.replace('#', '').strip()
        page_titles[page.name] = title

    # 使用 LLM 检测相似页面
    prompt = f"""Analyze these {category} page titles and find semantically similar pairs.

Titles:
{chr(10).join(f"- {name}: {title}" for name, title in page_titles.items())}

Find pairs that refer to the same concept/entity but with different names.
Examples of similar pairs:
- "MIPI 接口" and "MIPI接口" (same with/without space)
- "GWCPHY" and "gwcphy" (case difference)
- "SerDes 差分对" and "SerDes Differential Pair" (translation)

Output format (one pair per line):
page1.md | page2.md | similarity_score

Only output pairs with similarity > {threshold}. If no similar pairs found, output "NONE".
"""

    response = llm.generate(prompt)

    # 解析响应
    similar_pairs = []
    if response.strip() == "NONE":
        return []

    for line in response.strip().split('\n'):
        if '|' not in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) == 3:
            try:
                page1, page2, score = parts
                similarity = float(score)
                if similarity >= threshold:
                    similar_pairs.append((page1, page2, similarity))
            except ValueError:
                continue

    return similar_pairs

def merge_pages(wiki_dir: Path, primary_page: str, secondary_page: str, llm: LLMProvider) -> str:
    """合并两个页面

    Args:
        wiki_dir: wiki 根目录
        primary_page: 主页面路径（相对）
        secondary_page: 次页面路径（相对）
        llm: LLM provider

    Returns:
        合并后的内容
    """
    primary_path = wiki_dir / primary_page
    secondary_path = wiki_dir / secondary_page

    primary_content = primary_path.read_text(encoding='utf-8')
    secondary_content = secondary_path.read_text(encoding='utf-8')

    # 使用 LLM 合并内容
    prompt = f"""Merge these two pages about the same concept/entity.

Primary page ({primary_page}):
{primary_content}

Secondary page ({secondary_page}):
{secondary_content}

Create a merged page that:
1. Uses the primary page's title
2. Combines all unique information from both pages
3. Removes duplicate information
4. Maintains clear structure
5. Preserves all important details

Output the merged content directly (no explanations):
"""

    merged_content = llm.generate(prompt)
    return merged_content

def update_references(wiki_dir: Path, old_page: str, new_page: str):
    """更新所有引用

    Args:
        wiki_dir: wiki 根目录
        old_page: 旧页面名（不含路径）
        new_page: 新页面名（不含路径）
    """
    old_name = old_page.replace('.md', '')
    new_name = new_page.replace('.md', '')

    # 遍历所有页面
    for page in wiki_dir.glob('**/*.md'):
        if page.name in ['index.md', 'log.md'] or 'archive' in str(page):
            continue

        content = page.read_text(encoding='utf-8')

        # 替换链接
        # [[old-page]] -> [[new-page]]
        # [[old-page|text]] -> [[new-page|text]]
        updated = re.sub(
            rf'\[\[{re.escape(old_name)}(\|[^\]]+)?\]\]',
            rf'[[{new_name}\1]]',
            content
        )

        if updated != content:
            page.write_text(updated, encoding='utf-8')

from pathlib import Path
from typing import List
import re

def lint_wiki(wiki_dir: Path) -> List[str]:
    """检查 wiki 健康状况"""
    issues = []

    pages = list(wiki_dir.glob('**/*.md'))
    page_names = {p.name for p in pages}

    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for link_text, link_target in links:
            if link_target.endswith('.md') and link_target not in page_names:
                issues.append(f"Broken link in {page.name}: {link_target}")

    linked_pages = set()
    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+\.md)\)', content)
        for _, link_target in links:
            linked_pages.add(link_target)

    for page in pages:
        if page.name not in linked_pages and page.name != 'index.md':
            issues.append(f"Orphaned page: {page.name}")

    return issues

from pathlib import Path
from typing import List
import re

def lint_wiki(wiki_dir: Path) -> List[str]:
    """检查单个 wiki 健康状况"""
    issues = []

    pages = list(wiki_dir.glob('**/*.md'))
    page_names = {p.name for p in pages}

    # 检查损坏的链接
    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            link_file = link.split('/')[-1]
            if not link_file.endswith('.md'):
                link_file += '.md'
            if link_file not in page_names and '/' not in link:
                issues.append(f"Broken link in {page.name}: {link}")

    # 检查孤立页面
    linked_pages = set()
    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            link_file = link.split('/')[-1]
            if not link_file.endswith('.md'):
                link_file += '.md'
            linked_pages.add(link_file)

    for page in pages:
        if page.name not in linked_pages and page.name != 'index.md' and page.name != 'log.md':
            issues.append(f"Orphaned page: {page.name}")

    return issues

def lint_dual_wiki(base_path: Path) -> List[str]:
    """检查双 wiki 系统健康状况"""
    issues = []

    wiki_dir = base_path / 'wiki'
    personal_dir = base_path / 'personal'

    # 检查各自的健康状况
    if wiki_dir.exists():
        wiki_issues = lint_wiki(wiki_dir)
        issues.extend([f"[wiki] {i}" for i in wiki_issues])

    if personal_dir.exists():
        personal_issues = lint_wiki(personal_dir)
        issues.extend([f"[personal] {i}" for i in personal_issues])

    # 检查跨库引用（wiki → personal 禁止）
    if wiki_dir.exists():
        for page in wiki_dir.glob('**/*.md'):
            content = page.read_text(encoding='utf-8')
            if 'personal/' in content or '[[personal' in content:
                issues.append(f"❌ {page.relative_to(base_path)} references personal/ (forbidden)")

    # 检查同名文件冲突（排除 index.md 和 log.md）
    if wiki_dir.exists() and personal_dir.exists():
        wiki_files = {p.relative_to(wiki_dir) for p in wiki_dir.glob('**/*.md')
                      if p.name not in ['index.md', 'log.md']}
        personal_files = {p.relative_to(personal_dir) for p in personal_dir.glob('**/*.md')
                          if p.name not in ['index.md', 'log.md']}
        conflicts = wiki_files & personal_files
        for conflict in conflicts:
            issues.append(f"⚠️ Name conflict: wiki/{conflict} vs personal/{conflict}")

    # 检查 index.md 规模
    for target in ['wiki', 'personal']:
        index_file = base_path / target / 'index.md'
        if index_file.exists():
            line_count = len(index_file.read_text(encoding='utf-8').split('\n'))
            if line_count > 500:
                issues.append(f"🔴 {target}/index.md: {line_count} lines (critical: >500) - 必须重构")
            elif line_count > 300:
                issues.append(f"⚠️ {target}/index.md: {line_count} lines (warning: >300) - 建议重构")

    return issues

from pathlib import Path
from datetime import datetime
from utils.file_ops import write_file

def init_wiki_structure(base_path: Path, target: str):
    """初始化 wiki 或 personal 目录结构"""
    wiki_path = base_path / target

    # 定义子目录
    if target == 'wiki':
        subdirs = ['sources', 'concepts', 'entities', 'comparisons', 'questions']
        overview = '客观知识库：外部资料、技术原理'
    else:  # personal
        subdirs = ['sources', 'concepts', 'entities', 'reflections']
        overview = '主观知识库：个人经历、项目、反思'

    # 创建子目录
    for subdir in subdirs:
        (wiki_path / subdir).mkdir(parents=True, exist_ok=True)

    # 创建 index.md
    index_sections = '\n'.join([f'## {s.title()} (0)\n' for s in subdirs])
    index_content = f"""# {target.title()} Index

Last updated: {datetime.now().strftime('%Y-%m-%d')}

## Overview
{overview}

{index_sections}
---

Total pages: 0
"""
    write_file(wiki_path / 'index.md', index_content)

    # 创建 log.md
    log_content = f"""# {target.title()} Log

## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] init | {target.title()} initialized

Created initial structure.
"""
    write_file(wiki_path / 'log.md', log_content)

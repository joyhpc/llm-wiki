from pathlib import Path
from datetime import datetime
from typing import Dict, List
from core.llm import LLMProvider
from core.index_manager import update_categorized_index
from utils.parser import parse_document
from utils.file_ops import write_file, append_file

def ingest_document(
    source_file: Path,
    wiki_dir: Path,
    index_file: Path,
    log_file: Path,
    llm: LLMProvider
) -> Dict[str, List[str]]:
    """导入文档到 wiki，返回创建的页面列表"""
    parsed = parse_document(source_file)
    content = parsed['content']

    target = wiki_dir.name  # wiki 或 personal

    prompt = f"""Extract and organize information from this document into a knowledge base.

Source file: {source_file.name}

Document content:
{content}

Create the following pages:

1. A summary page in sources/ directory
2. Relevant concept pages in concepts/ directory
3. Relevant entity pages in entities/ directory

Use this exact output format:

PAGE: sources/document-name.md
CONTENT:
# Document Title
Summary of the document.
---
PAGE: concepts/concept-name.md
CONTENT:
# Concept Name
Explanation of the concept.
---

Start your response with "PAGE:" immediately.
"""

    response = llm.generate(prompt)
    pages = _parse_multi_page_response(response)

    # 写入所有页面
    created_pages = []
    for page_path, page_content in pages.items():
        full_path = wiki_dir / page_path
        write_file(full_path, page_content)
        created_pages.append(page_path)

    # 更新分类索引
    update_categorized_index(wiki_dir, created_pages)

    # 更新 log.md
    log_entry = f"## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] ingest | {source_file.name} → {len(created_pages)} pages\n\n"
    if log_file.exists():
        append_file(log_file, log_entry)
    else:
        write_file(log_file, log_entry)

    # 删除源文件
    source_file.unlink()

    return {'pages': created_pages}

def _parse_multi_page_response(response: str) -> Dict[str, str]:
    """解析 LLM 多页面响应"""
    pages = {}
    lines = response.split('\n')
    current_page = None
    current_content = []
    in_content = False

    for line in lines:
        if line.startswith('PAGE:'):
            if current_page and current_content:
                pages[current_page] = '\n'.join(current_content).strip()
            current_page = line.replace('PAGE:', '').strip()
            current_content = []
            in_content = False
        elif line.startswith('CONTENT:'):
            in_content = True
        elif line == '---':
            if current_page and current_content:
                pages[current_page] = '\n'.join(current_content).strip()
            current_page = None
            current_content = []
            in_content = False
        elif in_content:
            current_content.append(line)

    if current_page and current_content:
        pages[current_page] = '\n'.join(current_content).strip()

    return pages

# 旧的 _update_index 函数已移除，使用 index_manager.py 中的 update_categorized_index

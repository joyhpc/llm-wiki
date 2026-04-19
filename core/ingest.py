from pathlib import Path
from datetime import datetime
from core.llm import LLMProvider
from utils.parser import parse_document
from utils.file_ops import write_file, append_file

def ingest_document(
    source_file: Path,
    wiki_dir: Path,
    index_file: Path,
    log_file: Path,
    llm: LLMProvider
):
    """导入文档到 wiki"""
    parsed = parse_document(source_file)
    content = parsed['content']

    prompt = f"""You are maintaining a wiki. A new document has been added.

Source file: {source_file.name}
Content:
{content}

Tasks:
1. Extract key information from this document
2. Decide which wiki page(s) to update or create
3. Generate the wiki page content in markdown format

Output format:
FILENAME: <page-name>.md
CONTENT:
<markdown content>
"""

    response = llm.generate(prompt)
    filename, page_content = _parse_llm_response(response)

    wiki_page = wiki_dir / filename
    write_file(wiki_page, page_content)

    log_entry = f"## [{datetime.now().strftime('%Y-%m-%d')}] ingest | Added {source_file.name} -> {filename}\n\n"
    if log_file.exists():
        append_file(log_file, log_entry)
    else:
        write_file(log_file, log_entry)

    return wiki_page

def _parse_llm_response(response: str) -> tuple[str, str]:
    """解析 LLM 响应，提取文件名和内容"""
    lines = response.split('\n')
    filename = None
    content_lines = []
    in_content = False

    for line in lines:
        if line.startswith('FILENAME:'):
            filename = line.replace('FILENAME:', '').strip()
        elif line.startswith('CONTENT:'):
            in_content = True
        elif in_content:
            content_lines.append(line)

    if not filename:
        filename = 'untitled.md'

    return filename, '\n'.join(content_lines).strip()

from pathlib import Path
from typing import Dict
import pypdf

def parse_document(file_path: Path) -> Dict[str, str]:
    """解析文档并返回内容"""
    suffix = file_path.suffix.lower()

    if suffix == '.md':
        return {
            'type': 'markdown',
            'content': file_path.read_text(encoding='utf-8')
        }
    elif suffix == '.txt':
        return {
            'type': 'text',
            'content': file_path.read_text(encoding='utf-8')
        }
    elif suffix == '.pdf':
        return {
            'type': 'pdf',
            'content': _parse_pdf(file_path)
        }
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

def _parse_pdf(file_path: Path) -> str:
    """解析 PDF 文件"""
    reader = pypdf.PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)

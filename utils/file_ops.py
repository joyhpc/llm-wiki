from pathlib import Path
from typing import Dict

def ensure_dirs(base_path: Path) -> Dict[str, Path]:
    """创建必要的目录结构"""
    dirs = {
        'raw': base_path / 'raw',
        'raw_assets': base_path / 'raw' / 'assets',
        'wiki': base_path / 'wiki'
    }
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    return dirs

def read_file(file_path: Path) -> str:
    """读取文件内容"""
    return file_path.read_text(encoding='utf-8')

def write_file(file_path: Path, content: str):
    """写入文件"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')

def append_file(file_path: Path, content: str):
    """追加内容到文件"""
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)

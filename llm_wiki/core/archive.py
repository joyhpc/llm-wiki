from pathlib import Path
from datetime import datetime
from typing import Optional
import shutil

def archive_old_version(wiki_dir: Path, page_path: str) -> Optional[Path]:
    """归档旧版本页面

    Args:
        wiki_dir: wiki 根目录
        page_path: 相对路径，如 "sources/document.md"

    Returns:
        归档后的路径，如果没有旧版本则返回 None
    """
    current_file = wiki_dir / page_path
    if not current_file.exists():
        return None

    # 创建归档目录
    parts = page_path.split('/')
    category = parts[0]  # sources, concepts, entities
    filename = parts[-1]

    archive_dir = wiki_dir / category / 'archive'
    archive_dir.mkdir(exist_ok=True)

    # 生成归档文件名（带时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name_without_ext = filename.replace('.md', '')
    archive_filename = f"{name_without_ext}_{timestamp}.md"
    archive_path = archive_dir / archive_filename

    # 移动旧版本
    shutil.move(str(current_file), str(archive_path))

    return archive_path

def get_archive_history(wiki_dir: Path, page_path: str) -> list[Path]:
    """获取页面的归档历史

    Args:
        wiki_dir: wiki 根目录
        page_path: 相对路径，如 "sources/document.md"

    Returns:
        归档文件列表，按时间倒序
    """
    parts = page_path.split('/')
    category = parts[0]
    filename = parts[-1]
    name_without_ext = filename.replace('.md', '')

    archive_dir = wiki_dir / category / 'archive'
    if not archive_dir.exists():
        return []

    # 查找所有归档版本
    pattern = f"{name_without_ext}_*.md"
    archives = sorted(archive_dir.glob(pattern), reverse=True)

    return archives

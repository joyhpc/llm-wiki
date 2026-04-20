from pathlib import Path
from typing import Dict, Set, List
import re

def build_reference_graph(wiki_dir: Path) -> Dict[str, Set[str]]:
    """构建页面引用关系图

    Args:
        wiki_dir: wiki 根目录

    Returns:
        引用关系字典 {page_name: {referenced_by_page1, referenced_by_page2, ...}}
    """
    # 反向引用图：被谁引用
    references = {}

    # 遍历所有页面
    for page in wiki_dir.glob('**/*.md'):
        if page.name in ['index.md', 'log.md'] or 'archive' in str(page) or 'index/' in str(page):
            continue

        content = page.read_text(encoding='utf-8')

        # 提取所有链接
        links = re.findall(r'\[\[([^\]|]+)', content)

        for link in links:
            # 标准化链接名
            link_name = link.strip()
            if not link_name.endswith('.md'):
                link_name += '.md'

            # 记录反向引用
            if link_name not in references:
                references[link_name] = set()
            references[link_name].add(page.name)

    return references

def get_referencing_pages(wiki_dir: Path, page_name: str) -> List[Path]:
    """获取引用指定页面的所有页面

    Args:
        wiki_dir: wiki 根目录
        page_name: 页面名（如 "gwcphy.md"）

    Returns:
        引用该页面的所有页面路径列表
    """
    referencing = []
    page_name_without_ext = page_name.replace('.md', '')

    for page in wiki_dir.glob('**/*.md'):
        if page.name in ['index.md', 'log.md'] or 'archive' in str(page) or 'index/' in str(page):
            continue

        content = page.read_text(encoding='utf-8')

        # 检查是否引用了目标页面
        pattern = rf'\[\[{re.escape(page_name_without_ext)}(\|[^\]]+)?\]\]'
        if re.search(pattern, content):
            referencing.append(page)

    return referencing

def notify_referencing_pages(wiki_dir: Path, updated_page: str, log_file: Path):
    """通知引用页面有更新

    在 log.md 中记录哪些页面引用了更新的页面，提示用户检查

    Args:
        wiki_dir: wiki 根目录
        updated_page: 更新的页面名
        log_file: 日志文件路径
    """
    referencing = get_referencing_pages(wiki_dir, updated_page)

    if not referencing:
        return

    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    log_entry = f"\n## [{timestamp}] cascade-update | {updated_page} 已更新\n\n"
    log_entry += f"以下页面引用了 {updated_page}，可能需要检查：\n\n"

    for page in referencing:
        rel_path = page.relative_to(wiki_dir)
        log_entry += f"- [[{rel_path}]]\n"

    log_entry += "\n"

    # 追加到日志
    if log_file.exists():
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    else:
        log_file.write_text(log_entry, encoding='utf-8')

def cascade_update_summary(wiki_dir: Path, updated_page: str) -> Dict[str, any]:
    """生成级联更新摘要

    Args:
        wiki_dir: wiki 根目录
        updated_page: 更新的页面名

    Returns:
        摘要信息字典
    """
    referencing = get_referencing_pages(wiki_dir, updated_page)

    # 按类别分组
    by_category = {'sources': [], 'concepts': [], 'entities': [], 'other': []}

    for page in referencing:
        rel_path = page.relative_to(wiki_dir)
        category = str(rel_path).split('/')[0]

        if category in by_category:
            by_category[category].append(str(rel_path))
        else:
            by_category['other'].append(str(rel_path))

    return {
        'updated_page': updated_page,
        'total_references': len(referencing),
        'by_category': {k: v for k, v in by_category.items() if v}
    }

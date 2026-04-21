from pathlib import Path
from typing import List

def update_categorized_index(wiki_dir: Path, new_pages: List[str]):
    """更新分类索引结构

    结构：
    - index.md - 主索引（分类链接）
    - index/sources.md - Sources 索引
    - index/concepts.md - Concepts 索引
    - index/entities.md - Entities 索引
    """
    index_dir = wiki_dir / 'index'
    index_dir.mkdir(exist_ok=True)

    # 按子目录分组
    categorized = {'sources': [], 'concepts': [], 'entities': []}
    for page in new_pages:
        parts = page.split('/')
        if len(parts) == 2:
            category = parts[0]
            if category in categorized:
                categorized[category].append(page)

    # 更新各分类索引
    for category, pages in categorized.items():
        if not pages:
            continue

        category_file = index_dir / f'{category}.md'

        # 读取现有内容
        if category_file.exists():
            content = category_file.read_text(encoding='utf-8')
            lines = content.split('\n')
        else:
            lines = [f'# {category.title()}', '']

        # 添加新链接（避免重复）
        existing_links = set(line.strip() for line in lines if line.startswith('- [['))
        for page in pages:
            link = f"- [[{page}]]"
            if link not in existing_links:
                lines.append(link)

        category_file.write_text('\n'.join(lines), encoding='utf-8')

    # 更新主 index.md
    main_index = wiki_dir / 'index.md'
    main_content = f"""# {wiki_dir.name.title()} Index

## Categories

- [[index/sources|Sources]] - Source documents and summaries
- [[index/concepts|Concepts]] - Technical concepts and methodologies
- [[index/entities|Entities]] - Projects, tools, and entities

## Quick Stats

- Sources: {len(list((wiki_dir / 'sources').glob('*.md')))} files
- Concepts: {len(list((wiki_dir / 'concepts').glob('*.md')))} files
- Entities: {len(list((wiki_dir / 'entities').glob('*.md')))} files
"""
    main_index.write_text(main_content, encoding='utf-8')

def rebuild_all_indexes(wiki_dir: Path):
    """重建所有索引（用于迁移现有数据）"""
    index_dir = wiki_dir / 'index'
    index_dir.mkdir(exist_ok=True)

    # 收集所有页面
    all_pages = []
    for category in ['sources', 'concepts', 'entities']:
        category_dir = wiki_dir / category
        if category_dir.exists():
            for file in category_dir.glob('*.md'):
                all_pages.append(f"{category}/{file.name}")

    # 清空现有分类索引
    for category in ['sources', 'concepts', 'entities']:
        category_file = index_dir / f'{category}.md'
        category_file.write_text(f'# {category.title()}\n\n', encoding='utf-8')

    # 重建索引
    update_categorized_index(wiki_dir, all_pages)

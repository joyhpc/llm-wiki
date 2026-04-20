#!/usr/bin/env python3
"""迁移脚本：重建分类索引结构"""

from pathlib import Path
from core.index_manager import rebuild_all_indexes

def main():
    base_path = Path.cwd()

    # 重建 wiki 索引
    wiki_dir = base_path / 'wiki'
    if wiki_dir.exists():
        print(f'重建 wiki/ 索引...')
        rebuild_all_indexes(wiki_dir)
        print(f'✓ wiki/ 索引重建完成')

    # 重建 personal 索引
    personal_dir = base_path / 'personal'
    if personal_dir.exists():
        print(f'重建 personal/ 索引...')
        rebuild_all_indexes(personal_dir)
        print(f'✓ personal/ 索引重建完成')

    print('\n索引迁移完成！')
    print('\n新结构：')
    print('  index.md - 主索引（分类链接）')
    print('  index/sources.md - Sources 索引')
    print('  index/concepts.md - Concepts 索引')
    print('  index/entities.md - Entities 索引')

if __name__ == '__main__':
    main()

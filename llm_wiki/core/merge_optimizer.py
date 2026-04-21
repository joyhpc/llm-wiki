from pathlib import Path
from typing import List, Tuple, Set, Dict

def build_merge_graph(similar_pairs: List[Tuple[str, str, float]]) -> Dict[str, Set[str]]:
    """构建合并图，找出所有需要合并到同一个主页面的页面组

    Args:
        similar_pairs: 相似页面对列表 [(page1, page2, score), ...]

    Returns:
        合并组字典 {primary_page: {secondary_page1, secondary_page2, ...}}
    """
    # 使用并查集找出连通分量
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    # 合并所有相似页面
    for page1, page2, _ in similar_pairs:
        union(page1, page2)

    # 按组分组
    groups = {}
    for page in parent.keys():
        root = find(page)
        if root not in groups:
            groups[root] = set()
        if page != root:
            groups[root].add(page)

    return groups

def optimize_merge_order(similar_pairs: List[Tuple[str, str, float]]) -> List[Tuple[str, List[str]]]:
    """优化合并顺序，避免重复处理

    Args:
        similar_pairs: 相似页面对列表

    Returns:
        合并任务列表 [(primary_page, [secondary_pages]), ...]
    """
    merge_groups = build_merge_graph(similar_pairs)

    # 转换为合并任务列表
    merge_tasks = []
    for primary, secondaries in merge_groups.items():
        if secondaries:  # 只处理有次页面的组
            merge_tasks.append((primary, sorted(list(secondaries))))

    return merge_tasks

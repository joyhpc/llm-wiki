# 查询完备性优化方案

## 问题

当前查询只搜索前 5 个结果，可能遗漏重要信息：
- 无语义搜索
- 无图谱扩展
- 上下文可能不完整

## 方案：多阶段检索管线

### 阶段 1：关键词搜索

```python
def keyword_search(wiki_dir: Path, query: str, max_results: int = 10) -> List[Dict]:
    """基于关键词的全文搜索"""
    # 使用 ripgrep 或 grep
    results = []
    for page in wiki_dir.glob('**/*.md'):
        if page.name in ['index.md', 'log.md']:
            continue
        
        content = page.read_text(encoding='utf-8')
        
        # 简单的关键词匹配
        if query.lower() in content.lower():
            # 计算相关度（关键词出现次数）
            score = content.lower().count(query.lower())
            results.append({
                'file': page,
                'score': score,
                'type': 'keyword'
            })
    
    # 按相关度排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:max_results]
```

### 阶段 2：图谱扩展

```python
def graph_expansion(initial_pages: List[Path], wiki_dir: Path, depth: int = 1) -> List[Path]:
    """基于引用关系扩展相关页面"""
    expanded = set(initial_pages)
    current_level = set(initial_pages)
    
    for _ in range(depth):
        next_level = set()
        
        for page in current_level:
            # 找到该页面引用的所有页面
            content = page.read_text(encoding='utf-8')
            links = re.findall(r'\[\[([^\]|]+)', content)
            
            for link in links:
                link_path = find_page_by_name(wiki_dir, link)
                if link_path and link_path not in expanded:
                    next_level.add(link_path)
                    expanded.add(link_path)
        
        current_level = next_level
        if not current_level:
            break
    
    return list(expanded)
```

### 阶段 3：智能上下文组装

```python
def assemble_context(pages: List[Path], max_tokens: int = 8000) -> str:
    """智能组装上下文，控制 token 数量"""
    context_parts = []
    current_tokens = 0
    
    # 按相关度排序（假设 pages 已排序）
    for page in pages:
        content = page.read_text(encoding='utf-8')
        
        # 估算 token 数（粗略：1 token ≈ 4 字符）
        estimated_tokens = len(content) // 4
        
        if current_tokens + estimated_tokens > max_tokens:
            # 截断内容
            remaining_tokens = max_tokens - current_tokens
            content = content[:remaining_tokens * 4]
            context_parts.append(f"From {page.name} (truncated):\n{content}")
            break
        
        context_parts.append(f"From {page.name}:\n{content}")
        current_tokens += estimated_tokens
    
    return '\n\n---\n\n'.join(context_parts)
```

### 完整查询流程

```python
def query_wiki_complete(question: str, wiki_dir: Path, llm: LLMProvider) -> Dict:
    """完备的查询流程"""
    
    # 1. 关键词搜索
    print("🔍 关键词搜索...")
    keyword_results = keyword_search(wiki_dir, question, max_results=10)
    
    if not keyword_results:
        return {'answer': 'No relevant information found.', 'sources': []}
    
    # 2. 图谱扩展（1 层）
    print("🕸️ 图谱扩展...")
    initial_pages = [r['file'] for r in keyword_results[:5]]
    expanded_pages = graph_expansion(initial_pages, wiki_dir, depth=1)
    
    print(f"   找到 {len(keyword_results)} 个直接匹配，扩展到 {len(expanded_pages)} 个相关页面")
    
    # 3. 智能上下文组装
    print("📦 组装上下文...")
    context = assemble_context(expanded_pages, max_tokens=8000)
    
    # 4. LLM 生成答案
    print("💬 生成答案...")
    prompt = f"""Answer the question based on the wiki pages below.

Question: {question}

Wiki pages:
{context}

Provide a comprehensive answer. Cite sources using [[page-name]] format.

Answer:"""
    
    answer = llm.generate(prompt)
    
    # 5. 提取引用
    cited_sources = re.findall(r'\[\[([^\]]+)\]\]', answer)
    
    return {
        'answer': answer,
        'sources': cited_sources,
        'stats': {
            'keyword_matches': len(keyword_results),
            'expanded_pages': len(expanded_pages),
            'context_tokens': len(context) // 4
        }
    }
```

---

## 优势

1. **更完备**：
   - 关键词搜索找到直接匹配
   - 图谱扩展找到相关内容
   - 不会遗漏重要信息

2. **可控**：
   - 可以调整扩展深度
   - 可以控制上下文大小
   - 可以查看统计信息

3. **高效**：
   - 先搜索后扩展，避免全量遍历
   - 智能截断，控制 token 消耗

---

## 实现优先级

1. **P0**：图谱扩展（1 层）
2. **P1**：智能上下文组装
3. **P2**：语义搜索（可选，需要向量数据库）

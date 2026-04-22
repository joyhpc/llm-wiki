# 知识解析质量优化方案

## 问题

当前单步摄入质量不够高：
- Prompt 过于简单
- 无质量验证
- 提取不够准确

## 方案：两步思维链摄入（借鉴 nashsu）

### 步骤 1：分析阶段

**目标**：深度理解文档，提取结构化信息

```python
def analyze_document(content: str, llm: LLMProvider) -> Dict:
    """第一步：分析文档"""
    prompt = f"""Analyze this document deeply and extract structured information.

Document:
{content}

Extract:
1. **Core Concepts**: Key ideas, theories, methods (with definitions)
2. **Entities**: People, tools, frameworks, organizations (with descriptions)
3. **Relationships**: How concepts relate to each other
4. **Contradictions**: Conflicting ideas or debates
5. **Questions**: Unanswered questions or areas for further research

Output as JSON:
{{
  "concepts": [
    {{"name": "...", "definition": "...", "importance": "high/medium/low"}}
  ],
  "entities": [
    {{"name": "...", "type": "person/tool/framework", "description": "..."}}
  ],
  "relationships": [
    {{"from": "concept1", "to": "concept2", "type": "depends_on/contradicts/extends"}}
  ],
  "contradictions": ["..."],
  "questions": ["..."]
}}
"""
    
    response = llm.generate(prompt)
    return json.loads(response)
```

### 步骤 2：生成阶段

**目标**：基于分析结果生成高质量页面

```python
def generate_pages(analysis: Dict, source_name: str, llm: LLMProvider) -> List[str]:
    """第二步：生成页面"""
    pages = []
    
    # 为每个概念生成页面
    for concept in analysis['concepts']:
        prompt = f"""Generate a wiki page for this concept.

Concept: {concept['name']}
Definition: {concept['definition']}
Importance: {concept['importance']}

Related concepts: {[r['to'] for r in analysis['relationships'] if r['from'] == concept['name']]}

Generate a comprehensive page with:
1. Clear definition
2. Detailed explanation
3. Examples
4. Relationships to other concepts
5. References

Format:
# {concept['name']}

## Definition
...

## Explanation
...

## Examples
...

## Related Concepts
- [[concept1]]
- [[concept2]]

## Source
- [[{source_name}]]
"""
        
        page_content = llm.generate(prompt)
        pages.append({
            'path': f"concepts/{slugify(concept['name'])}.md",
            'content': page_content
        })
    
    return pages
```

### 完整流程

```python
def ingest_document_two_step(source_file: Path, wiki_dir: Path, llm: LLMProvider):
    # 1. 解析文档
    content = parse_document(source_file)
    
    # 2. 分析阶段（提取结构化信息）
    print("📊 分析文档...")
    analysis = analyze_document(content, llm)
    
    # 3. 质量检查
    if len(analysis['concepts']) == 0:
        print("⚠ 未提取到概念，可能是文档质量问题")
        return
    
    # 4. 生成阶段（创建页面）
    print(f"📝 生成 {len(analysis['concepts'])} 个概念页面...")
    pages = generate_pages(analysis, source_file.name, llm)
    
    # 5. 写入文件
    for page in pages:
        write_file(wiki_dir / page['path'], page['content'])
    
    # 6. 更新索引
    update_index(wiki_dir, pages)
    
    print(f"✓ 完成！生成 {len(pages)} 个页面")
```

---

## 优势

1. **质量更高**：
   - 分析阶段深度理解
   - 生成阶段有结构化输入
   - 提取更准确

2. **可验证**：
   - 分析结果是 JSON，可检查
   - 可以人工审核分析结果
   - 可以调整生成策略

3. **可扩展**：
   - 可以添加更多分析维度
   - 可以自定义生成模板
   - 可以插入人工审核环节

---

## 实现优先级

1. **P0**：两步摄入基础实现
2. **P1**：质量检查和验证
3. **P2**：人工审核接口

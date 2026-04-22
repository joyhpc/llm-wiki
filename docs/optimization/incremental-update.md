# 知识更新优化方案

## 问题

当前 ingest 每次都完全重新处理文档，无法：
1. 检测文档是否已存在
2. 识别文档内容是否变更
3. 增量更新变更部分
4. 保留未变更的页面

## 方案：增量更新机制

### 1. 文档指纹（SHA256）

```python
import hashlib

def compute_file_hash(file_path: Path) -> str:
    """计算文件 SHA256 哈希"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
```

### 2. 摄入记录（.llm_wiki/ingest_cache.json）

```json
{
  "transformer-paper.pdf": {
    "hash": "abc123...",
    "ingested_at": "2026-04-22T10:00:00",
    "generated_pages": [
      "wiki/sources/transformer-paper.md",
      "wiki/concepts/attention-mechanism.md",
      "wiki/concepts/transformer-architecture.md"
    ]
  }
}
```

### 3. 增量更新流程

```python
def ingest_document_incremental(source_file: Path, wiki_dir: Path, llm: LLMProvider):
    # 1. 计算文件哈希
    current_hash = compute_file_hash(source_file)
    
    # 2. 检查缓存
    cache = load_ingest_cache(wiki_dir)
    cache_key = source_file.name
    
    if cache_key in cache:
        cached_hash = cache[cache_key]['hash']
        
        # 3. 未变更 → 跳过
        if current_hash == cached_hash:
            print(f"✓ {source_file.name} 未变更，跳过")
            return
        
        # 4. 已变更 → 增量更新
        print(f"⚠ {source_file.name} 已变更，增量更新")
        old_pages = cache[cache_key]['generated_pages']
        
        # 归档旧版本
        for page in old_pages:
            archive_old_version(Path(page))
        
        # 重新摄入
        new_pages = ingest_document(source_file, wiki_dir, llm)
        
        # 级联通知
        for page in new_pages:
            notify_referencing_pages(wiki_dir, page, log_file)
    else:
        # 5. 新文档 → 完整摄入
        print(f"✓ {source_file.name} 是新文档，完整摄入")
        new_pages = ingest_document(source_file, wiki_dir, llm)
    
    # 6. 更新缓存
    cache[cache_key] = {
        'hash': current_hash,
        'ingested_at': datetime.now().isoformat(),
        'generated_pages': new_pages
    }
    save_ingest_cache(wiki_dir, cache)
```

### 4. 优势

- ✅ 避免重复摄入（节省 token）
- ✅ 检测文档变更
- ✅ 自动归档旧版本
- ✅ 级联通知引用页面
- ✅ 保留摄入历史

---

## 实现优先级

1. **P0**：文档指纹 + 缓存检测
2. **P1**：增量更新流程
3. **P2**：智能 diff（只更新变更部分）

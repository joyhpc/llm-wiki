---
name: Dual Wiki Architecture Refactoring
description: 重构为 wiki + personal 双知识库架构，基于 Karpathy gist
type: design
---

# 双 Wiki 架构重构设计

## 概述

基于 https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f 的 LLM Wiki 模式，重构为双知识库系统：
- **wiki/** - 客观知识（外部资料、技术原理）
- **personal/** - 主观知识（个人经历、项目、反思）

两个库完全同构但严格隔离，避免知识污染。

## 架构设计

### 目录结构

```
HPC_VAULT/
├── .claude/
│   └── CLAUDE.md          # 路由规则、Lint 规则、Schema 定义
├── wiki/                  # 客观知识库
│   ├── index.md           # 主索引
│   ├── log.md             # 操作日志
│   ├── sources/           # 外部文章、论文
│   ├── concepts/          # 技术原理、方法论
│   ├── entities/          # 工具、人物、组织
│   ├── comparisons/       # 技术对比
│   └── questions/         # 问答记录
├── personal/              # 主观知识库（同构）
│   ├── index.md
│   ├── log.md
│   ├── sources/           # 个人经历、项目日志
│   ├── concepts/          # 个人方法论、经验
│   ├── entities/          # 我的项目、作品
│   └── reflections/       # 深度反思、决策
├── raw/                   # 待处理文档
│   └── assets/            # 图片、媒体
├── core/                  # Python 核心代码
├── utils/                 # 工具函数
└── wiki_cli.py            # CLI 入口
```

### 核心机制

**1. 路由规则**
- `ingest <file>` → 默认路由到 wiki/
- `ingest personal <file>` → 路由到 personal/
- `query <question>` → 自动检测（默认 wiki，触发词：personal/我的/我之前）
- `lint` → 检查两个库 + 交叉引用 + 规模监控

**2. 隔离保证**
- ✅ personal → wiki 引用（允许）
- ❌ wiki → personal 引用（禁止，Lint 报错）
- 命名规范：personal/concepts/ 加前缀避免冲突

**3. 规模监控**
- Lint 自动检查 index.md 行数
- 300 行警告，500 行严重
- 触发时提示重构为分层 index

## 功能设计

### Ingest 流程（无讨论，直接执行）

1. 读取 raw/ 源文档
2. LLM 提取信息，创建 sources/ 摘要页
3. 更新相关 concepts/ 和 entities/ 页面
4. 更新 index.md（添加新页面链接）
5. 追加 log.md 条目
6. **删除 raw/ 源文件**（处理后清理）
7. 一句话报告：处理了什么，创建了几个页面

**LLM Prompt 模板**：
```
You are maintaining a {target} knowledge base (wiki or personal).

Source: {filename}
Content: {content}

Tasks:
1. Create summary page in {target}/sources/
2. Update relevant pages in {target}/concepts/ and {target}/entities/
3. Return structured output with all page updates

Output format:
PAGES:
- sources/{name}.md: {content}
- concepts/{name}.md: {content}
- entities/{name}.md: {content}
```

### Query 流程（自动路由）

**路由逻辑**：
```python
def detect_target(question: str) -> str:
    # 触发 personal 的关键词
    personal_triggers = ['personal', '我的', '我之前', '我曾经']
    if any(t in question.lower() for t in personal_triggers):
        return 'personal'
    return 'wiki'  # 默认
```

**查询流程**：
1. 检测目标库（wiki 或 personal）
2. 读取 {target}/index.md 找相关页面
3. 读取相关页面内容
4. LLM 合成答案并引用来源
5. 如果答案有价值，可选择保存为新页面

### Lint 增强（跨库检查 + 规模监控）

**检查项**：
1. 页面内矛盾（每个库内部）
2. 过时声明
3. 孤立页面（无入链）
4. 缺失交叉引用
5. **❌ wiki → personal 引用**（报错）
6. **同名文件冲突**（wiki/concepts/xxx.md vs personal/concepts/xxx.md）
7. **死链接**（personal 引用的 wiki 页面不存在）
8. **规模监控**：
   - wiki/index.md 或 personal/index.md 超过 300 行 → ⚠️ 警告
   - 超过 500 行 → 🔴 严重

**报告格式**：
```
Wiki Health Check:
✓ No contradictions
✓ No orphaned pages
⚠️ wiki/index.md: 350 lines (threshold: 300) - 建议重构为分层索引
❌ wiki/concepts/foo.md references personal/reflections/bar.md (forbidden)

Personal Health Check:
✓ All checks passed
```

## 技术实现

### 代码改动

**1. CLI 层（wiki_cli.py）**
```python
@cli.command()
@click.argument('target', default='wiki')
@click.argument('file', type=click.Path(exists=True))
def ingest(target, file):
    """导入文档到 wiki 或 personal"""
    if target not in ['wiki', 'personal']:
        # 如果第一个参数是文件路径，target 默认为 wiki
        file, target = target, 'wiki'
    
    config = _load_config()
    llm = _create_llm(config)
    
    source_file = Path(file)
    wiki_dir = Path(config['paths'][target])
    index_file = wiki_dir / 'index.md'
    log_file = wiki_dir / 'log.md'
    
    result = ingest_document(source_file, wiki_dir, index_file, log_file, llm)
    
    # 删除源文件
    source_file.unlink()
    
    click.echo(f'✓ 处理 {source_file.name}，创建 {len(result["pages"])} 个页面')
```

**2. Ingest 层（core/ingest.py）**
- 修改 `ingest_document()` 返回多页面结果
- 支持创建子目录页面（sources/, concepts/, entities/）
- 更新 index.md 逻辑
- 删除源文件

**3. Query 层（core/query.py）**
- 添加 `detect_target()` 函数
- 修改 `query_wiki()` 支持目标参数

**4. Lint 层（core/lint.py）**
- 添加 `lint_cross_references()` 检查跨库引用
- 添加 `check_index_size()` 规模监控
- 添加 `check_name_conflicts()` 同名检查

**5. 配置文件（config.yaml）**
```yaml
llm:
  provider: claude
  model: claude-opus-4-6
  api_key: ${ANTHROPIC_API_KEY}

paths:
  wiki: ./wiki
  personal: ./personal
  raw: ./raw

lint:
  index_warning_lines: 300
  index_critical_lines: 500
```

### 初始化脚本

创建 `init_dual_wiki.py`：
```python
def init_dual_wiki():
    """初始化双 wiki 结构"""
    for target in ['wiki', 'personal']:
        base = Path(target)
        
        # 创建子目录
        subdirs = ['sources', 'concepts', 'entities']
        if target == 'wiki':
            subdirs += ['comparisons', 'questions']
        else:
            subdirs += ['reflections']
        
        for subdir in subdirs:
            (base / subdir).mkdir(parents=True, exist_ok=True)
        
        # 创建 index.md
        index_content = f"""# {target.title()} Index

Last updated: {datetime.now().strftime('%Y-%m-%d')}

## Overview
{'客观知识库：外部资料、技术原理' if target == 'wiki' else '主观知识库：个人经历、项目、反思'}

{generate_index_sections(subdirs)}

---

Total pages: 0
"""
        write_file(base / 'index.md', index_content)
        
        # 创建 log.md
        log_content = f"""# {target.title()} Log

## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] init | {target.title()} initialized

Created initial structure.
"""
        write_file(base / 'log.md', log_content)
```

## 数据流

### Ingest 数据流
```
raw/doc.md 
  → LLM 分析 
  → 创建 sources/doc-summary.md
  → 更新 concepts/*.md
  → 更新 entities/*.md
  → 更新 index.md
  → 追加 log.md
  → 删除 raw/doc.md
  → 报告结果
```

### Query 数据流
```
用户问题
  → detect_target() 判断 wiki/personal
  → 读取 {target}/index.md
  → 搜索相关页面
  → LLM 合成答案
  → 返回带引用的回答
```

### Lint 数据流
```
触发 lint
  → 检查 wiki/ 健康
  → 检查 personal/ 健康
  → 检查跨库引用（wiki → personal 禁止）
  → 检查同名冲突
  → 检查 index.md 规模
  → 生成报告
```

## 错误处理

- 源文件不存在：报错，不删除
- LLM 生成失败：保留源文件，报错
- Index 更新失败：回滚，保留源文件
- 跨库引用检测：Lint 报错但不阻止操作

## 测试策略

- 单元测试：各模块独立测试
- 集成测试：完整 ingest/query/lint 流程
- 跨库测试：验证隔离规则
- 规模测试：模拟 300+ 行 index

## 未来扩展

- 分层 index 自动重构
- 可视化知识图谱
- 版本控制（wiki 页面历史）
- 多用户协作

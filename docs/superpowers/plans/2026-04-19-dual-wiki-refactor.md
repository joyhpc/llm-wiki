# 双 Wiki 架构重构实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构为 wiki + personal 双知识库架构，支持路由、隔离检查和规模监控

**Architecture:** 扩展现有单 wiki 架构，添加 personal/ 目录，修改 CLI 支持路由，增强 ingest/query/lint 功能

**Tech Stack:** Python 3.10+, click, anthropic SDK, ollama, pyyaml

---

## File Structure

```
HPC_VAULT/
├── .claude/
│   └── CLAUDE.md              # 新建：Schema 和规则定义
├── wiki/                      # 新建目录结构
│   ├── index.md
│   ├── log.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   ├── comparisons/
│   └── questions/
├── personal/                  # 新建目录结构
│   ├── index.md
│   ├── log.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   └── reflections/
├── core/
│   ├── ingest.py             # 修改：支持多页面、子目录、删除源文件
│   ├── query.py              # 修改：添加目标检测
│   ├── lint.py               # 修改：跨库检查、规模监控
│   └── router.py             # 新建：路由逻辑
├── utils/
│   └── init_wiki.py          # 新建：初始化工具
└── wiki_cli.py               # 修改：CLI 路由
```

### Task 1: 创建初始化工具

**Files:**
- Create: `utils/init_wiki.py`
- Create: `tests/test_init_wiki.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_init_wiki.py
import pytest
from pathlib import Path
from utils.init_wiki import init_wiki_structure

def test_init_wiki_structure(tmp_path):
    init_wiki_structure(tmp_path, 'wiki')
    
    assert (tmp_path / 'wiki' / 'index.md').exists()
    assert (tmp_path / 'wiki' / 'log.md').exists()
    assert (tmp_path / 'wiki' / 'sources').is_dir()
    assert (tmp_path / 'wiki' / 'concepts').is_dir()
    assert (tmp_path / 'wiki' / 'entities').is_dir()
    assert (tmp_path / 'wiki' / 'comparisons').is_dir()
    assert (tmp_path / 'wiki' / 'questions').is_dir()

def test_init_personal_structure(tmp_path):
    init_wiki_structure(tmp_path, 'personal')
    
    assert (tmp_path / 'personal' / 'index.md').exists()
    assert (tmp_path / 'personal' / 'log.md').exists()
    assert (tmp_path / 'personal' / 'reflections').is_dir()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `source venv/bin/activate && python -m pytest tests/test_init_wiki.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: 实现初始化工具**

```python
# utils/init_wiki.py
from pathlib import Path
from datetime import datetime
from utils.file_ops import write_file

def init_wiki_structure(base_path: Path, target: str):
    """初始化 wiki 或 personal 目录结构"""
    wiki_path = base_path / target
    
    # 定义子目录
    if target == 'wiki':
        subdirs = ['sources', 'concepts', 'entities', 'comparisons', 'questions']
        overview = '客观知识库：外部资料、技术原理'
    else:  # personal
        subdirs = ['sources', 'concepts', 'entities', 'reflections']
        overview = '主观知识库：个人经历、项目、反思'
    
    # 创建子目录
    for subdir in subdirs:
        (wiki_path / subdir).mkdir(parents=True, exist_ok=True)
    
    # 创建 index.md
    index_sections = '\n'.join([f'## {s.title()} (0)\n' for s in subdirs])
    index_content = f"""# {target.title()} Index

Last updated: {datetime.now().strftime('%Y-%m-%d')}

## Overview
{overview}

{index_sections}
---

Total pages: 0
"""
    write_file(wiki_path / 'index.md', index_content)
    
    # 创建 log.md
    log_content = f"""# {target.title()} Log

## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] init | {target.title()} initialized

Created initial structure.
"""
    write_file(wiki_path / 'log.md', log_content)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `source venv/bin/activate && python -m pytest tests/test_init_wiki.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add utils/init_wiki.py tests/test_init_wiki.py
git commit -m "feat: add wiki initialization utility"
```

### Task 2: 创建路由模块

**Files:**
- Create: `core/router.py`
- Create: `tests/test_router.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_router.py
import pytest
from core.router import detect_query_target

def test_detect_wiki_default():
    assert detect_query_target("What is Transformer?") == "wiki"
    assert detect_query_target("Explain attention mechanism") == "wiki"

def test_detect_personal_keywords():
    assert detect_query_target("我的项目架构是什么？") == "personal"
    assert detect_query_target("我之前怎么处理的？") == "personal"
    assert detect_query_target("查 personal：反思记录") == "personal"
    assert detect_query_target("What did I do in project X?") == "personal"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `source venv/bin/activate && python -m pytest tests/test_router.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: 实现路由模块**

```python
# core/router.py
def detect_query_target(question: str) -> str:
    """检测查询目标：wiki 或 personal"""
    question_lower = question.lower()
    
    # personal 触发词
    personal_triggers = [
        'personal', '我的', '我之前', '我曾经', 
        'my ', 'i did', 'i have', 'i worked'
    ]
    
    for trigger in personal_triggers:
        if trigger in question_lower:
            return 'personal'
    
    return 'wiki'  # 默认
```

- [ ] **Step 4: 运行测试确认通过**

Run: `source venv/bin/activate && python -m pytest tests/test_router.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/router.py tests/test_router.py
git commit -m "feat: add query routing logic"
```

### Task 3: 增强 Ingest 支持多页面和子目录

**Files:**
- Modify: `core/ingest.py`
- Modify: `tests/test_ingest.py`

- [ ] **Step 1: 写增强测试**

```python
# tests/test_ingest.py（追加）
def test_ingest_creates_subdirectory_pages(tmp_path):
    raw_file = tmp_path / "raw" / "test.md"
    raw_file.parent.mkdir()
    raw_file.write_text("# AI Article\n\nTransformers are neural networks")
    
    wiki_dir = tmp_path / "wiki"
    (wiki_dir / "sources").mkdir(parents=True)
    (wiki_dir / "concepts").mkdir(parents=True)
    index_file = wiki_dir / "index.md"
    log_file = wiki_dir / "log.md"
    
    llm = MockLLM()
    result = ingest_document(raw_file, wiki_dir, index_file, log_file, llm)
    
    assert 'pages' in result
    assert len(result['pages']) > 0
    assert not raw_file.exists()  # 源文件已删除

def test_ingest_updates_index(tmp_path):
    raw_file = tmp_path / "raw" / "test.md"
    raw_file.parent.mkdir()
    raw_file.write_text("Content")
    
    wiki_dir = tmp_path / "wiki"
    (wiki_dir / "sources").mkdir(parents=True)
    index_file = wiki_dir / "index.md"
    index_file.write_text("# Index\n\n## Sources (0)\n")
    log_file = wiki_dir / "log.md"
    
    llm = MockLLM()
    ingest_document(raw_file, wiki_dir, index_file, log_file, llm)
    
    index_content = index_file.read_text()
    assert "## Sources (1)" in index_content or "sources/" in index_content
```

- [ ] **Step 2: 运行测试确认失败**

Run: `source venv/bin/activate && python -m pytest tests/test_ingest.py::test_ingest_creates_subdirectory_pages -v`
Expected: FAIL

- [ ] **Step 3: 重构 ingest_document 支持多页面**

```python
# core/ingest.py（完全替换）
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from core.llm import LLMProvider
from utils.parser import parse_document
from utils.file_ops import write_file, append_file

def ingest_document(
    source_file: Path,
    wiki_dir: Path,
    index_file: Path,
    log_file: Path,
    llm: LLMProvider
) -> Dict[str, List[str]]:
    """导入文档到 wiki，返回创建的页面列表"""
    parsed = parse_document(source_file)
    content = parsed['content']
    
    target = wiki_dir.name  # wiki 或 personal
    
    prompt = f"""You are maintaining a {target} knowledge base.

Source: {source_file.name}
Content:
{content}

Tasks:
1. Create summary page in sources/
2. Update or create relevant pages in concepts/ and entities/
3. Return structured output

Output format (one page per line):
PAGE: sources/filename.md
CONTENT:
<markdown content>
---
PAGE: concepts/concept-name.md
CONTENT:
<markdown content>
---
"""
    
    response = llm.generate(prompt)
    pages = _parse_multi_page_response(response)
    
    # 写入所有页面
    created_pages = []
    for page_path, page_content in pages.items():
        full_path = wiki_dir / page_path
        write_file(full_path, page_content)
        created_pages.append(page_path)
    
    # 更新 index.md
    _update_index(index_file, created_pages)
    
    # 更新 log.md
    log_entry = f"## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] ingest | {source_file.name} → {len(created_pages)} pages\n\n"
    if log_file.exists():
        append_file(log_file, log_entry)
    else:
        write_file(log_file, log_entry)
    
    # 删除源文件
    source_file.unlink()
    
    return {'pages': created_pages}

def _parse_multi_page_response(response: str) -> Dict[str, str]:
    """解析 LLM 多页面响应"""
    pages = {}
    lines = response.split('\n')
    current_page = None
    current_content = []
    in_content = False
    
    for line in lines:
        if line.startswith('PAGE:'):
            if current_page and current_content:
                pages[current_page] = '\n'.join(current_content).strip()
            current_page = line.replace('PAGE:', '').strip()
            current_content = []
            in_content = False
        elif line.startswith('CONTENT:'):
            in_content = True
        elif line == '---':
            if current_page and current_content:
                pages[current_page] = '\n'.join(current_content).strip()
            current_page = None
            current_content = []
            in_content = False
        elif in_content:
            current_content.append(line)
    
    if current_page and current_content:
        pages[current_page] = '\n'.join(current_content).strip()
    
    return pages

def _update_index(index_file: Path, new_pages: List[str]):
    """更新 index.md 添加新页面链接"""
    if not index_file.exists():
        return
    
    content = index_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 按子目录分组
    for page in new_pages:
        subdir = page.split('/')[0]
        link = f"- [[{page}]]"
        
        # 找到对应的 section 并添加链接
        section_header = f"## {subdir.title()}"
        for i, line in enumerate(lines):
            if line.startswith(section_header):
                # 在下一个空行或下一个 ## 之前插入
                j = i + 1
                while j < len(lines) and not lines[j].startswith('##') and lines[j].strip():
                    j += 1
                lines.insert(j, link)
                break
    
    write_file(index_file, '\n'.join(lines))
```

- [ ] **Step 4: 运行测试确认通过**

Run: `source venv/bin/activate && python -m pytest tests/test_ingest.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/ingest.py tests/test_ingest.py
git commit -m "feat: enhance ingest to support multi-page and subdirectories"
```

### Task 4: 增强 Query 支持目标检测

**Files:**
- Modify: `core/query.py`
- Modify: `tests/test_query.py`

- [ ] **Step 1: 写增强测试**

```python
# tests/test_query.py（追加）
from core.router import detect_query_target

def test_query_with_target_detection(tmp_path):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    (wiki_dir / "concepts").mkdir()
    (wiki_dir / "concepts" / "ai.md").write_text("# AI\n\nAI is artificial intelligence")
    
    personal_dir = tmp_path / "personal"
    personal_dir.mkdir()
    (personal_dir / "reflections").mkdir()
    (personal_dir / "reflections" / "project.md").write_text("# Project\n\nI built X")
    
    llm = MockLLM()
    
    # 默认查 wiki
    result = query_wiki_auto("What is AI?", tmp_path, llm)
    assert 'ai' in result['answer'].lower()
    
    # 触发 personal
    result = query_wiki_auto("我的项目是什么？", tmp_path, llm)
    assert 'project' in result['answer'].lower()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `source venv/bin/activate && python -m pytest tests/test_query.py::test_query_with_target_detection -v`
Expected: FAIL with "NameError: name 'query_wiki_auto' is not defined"

- [ ] **Step 3: 实现自动路由查询**

```python
# core/query.py（追加到文件末尾）
from core.router import detect_query_target

def query_wiki_auto(question: str, base_path: Path, llm: LLMProvider) -> Dict[str, str]:
    """自动检测目标并查询"""
    target = detect_query_target(question)
    wiki_dir = base_path / target
    return query_wiki(question, wiki_dir, llm)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `source venv/bin/activate && python -m pytest tests/test_query.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/query.py tests/test_query.py
git commit -m "feat: add auto-routing query support"
```

### Task 5: 增强 Lint 支持跨库检查和规模监控

**Files:**
- Modify: `core/lint.py`
- Modify: `tests/test_lint.py`

- [ ] **Step 1: 写增强测试**

```python
# tests/test_lint.py（追加）
def test_lint_forbids_wiki_to_personal_refs(tmp_path):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    (wiki_dir / "concepts").mkdir()
    (wiki_dir / "concepts" / "foo.md").write_text("See [[personal/reflections/bar.md]]")
    
    personal_dir = tmp_path / "personal"
    personal_dir.mkdir()
    
    issues = lint_dual_wiki(tmp_path)
    assert any('wiki → personal' in i.lower() for i in issues)

def test_lint_allows_personal_to_wiki_refs(tmp_path):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    (wiki_dir / "concepts").mkdir()
    (wiki_dir / "concepts" / "ai.md").write_text("# AI")
    
    personal_dir = tmp_path / "personal"
    personal_dir.mkdir()
    (personal_dir / "reflections").mkdir()
    (personal_dir / "reflections" / "project.md").write_text("Used [[wiki/concepts/ai.md]]")
    
    issues = lint_dual_wiki(tmp_path)
    assert not any('personal → wiki' in i.lower() for i in issues)

def test_lint_checks_index_size(tmp_path):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    index_file = wiki_dir / "index.md"
    
    # 创建超过 300 行的 index
    large_content = "# Index\n" + "\n".join([f"- Page {i}" for i in range(350)])
    index_file.write_text(large_content)
    
    issues = lint_dual_wiki(tmp_path)
    assert any('300' in i and 'index.md' in i for i in issues)

def test_lint_checks_name_conflicts(tmp_path):
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    (wiki_dir / "concepts").mkdir()
    (wiki_dir / "concepts" / "foo.md").write_text("# Foo")
    
    personal_dir = tmp_path / "personal"
    personal_dir.mkdir()
    (personal_dir / "concepts").mkdir()
    (personal_dir / "concepts" / "foo.md").write_text("# My Foo")
    
    issues = lint_dual_wiki(tmp_path)
    assert any('conflict' in i.lower() and 'foo.md' in i for i in issues)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `source venv/bin/activate && python -m pytest tests/test_lint.py::test_lint_forbids_wiki_to_personal_refs -v`
Expected: FAIL with "NameError: name 'lint_dual_wiki' is not defined"

- [ ] **Step 3: 实现双 wiki Lint**

```python
# core/lint.py（完全替换）
from pathlib import Path
from typing import List
import re

def lint_wiki(wiki_dir: Path) -> List[str]:
    """检查单个 wiki 健康状况"""
    issues = []
    
    pages = list(wiki_dir.glob('**/*.md'))
    page_names = {p.name for p in pages}
    
    # 检查损坏的链接
    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            link_file = link.split('/')[-1]
            if not link_file.endswith('.md'):
                link_file += '.md'
            if link_file not in page_names and '/' not in link:
                issues.append(f"Broken link in {page.name}: {link}")
    
    # 检查孤立页面
    linked_pages = set()
    for page in pages:
        content = page.read_text(encoding='utf-8')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            link_file = link.split('/')[-1]
            if not link_file.endswith('.md'):
                link_file += '.md'
            linked_pages.add(link_file)
    
    for page in pages:
        if page.name not in linked_pages and page.name != 'index.md' and page.name != 'log.md':
            issues.append(f"Orphaned page: {page.name}")
    
    return issues

def lint_dual_wiki(base_path: Path) -> List[str]:
    """检查双 wiki 系统健康状况"""
    issues = []
    
    wiki_dir = base_path / 'wiki'
    personal_dir = base_path / 'personal'
    
    # 检查各自的健康状况
    if wiki_dir.exists():
        wiki_issues = lint_wiki(wiki_dir)
        issues.extend([f"[wiki] {i}" for i in wiki_issues])
    
    if personal_dir.exists():
        personal_issues = lint_wiki(personal_dir)
        issues.extend([f"[personal] {i}" for i in personal_issues])
    
    # 检查跨库引用（wiki → personal 禁止）
    if wiki_dir.exists():
        for page in wiki_dir.glob('**/*.md'):
            content = page.read_text(encoding='utf-8')
            if 'personal/' in content or '[[personal' in content:
                issues.append(f"❌ {page.relative_to(base_path)} references personal/ (forbidden)")
    
    # 检查同名文件冲突
    if wiki_dir.exists() and personal_dir.exists():
        wiki_files = {p.relative_to(wiki_dir) for p in wiki_dir.glob('**/*.md')}
        personal_files = {p.relative_to(personal_dir) for p in personal_dir.glob('**/*.md')}
        conflicts = wiki_files & personal_files
        for conflict in conflicts:
            issues.append(f"⚠️ Name conflict: wiki/{conflict} vs personal/{conflict}")
    
    # 检查 index.md 规模
    for target in ['wiki', 'personal']:
        index_file = base_path / target / 'index.md'
        if index_file.exists():
            line_count = len(index_file.read_text(encoding='utf-8').split('\n'))
            if line_count > 500:
                issues.append(f"🔴 {target}/index.md: {line_count} lines (critical: >500) - 必须重构")
            elif line_count > 300:
                issues.append(f"⚠️ {target}/index.md: {line_count} lines (warning: >300) - 建议重构")
    
    return issues
```

- [ ] **Step 4: 运行测试确认通过**

Run: `source venv/bin/activate && python -m pytest tests/test_lint.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/lint.py tests/test_lint.py
git commit -m "feat: enhance lint with cross-wiki checks and size monitoring"
```

### Task 6: 更新 CLI 支持路由

**Files:**
- Modify: `wiki_cli.py`

- [ ] **Step 1: 修改 init 命令支持双 wiki**

```python
# wiki_cli.py（修改 init 命令）
from utils.init_wiki import init_wiki_structure

@cli.command()
def init():
    """初始化 wiki 和 personal 目录结构"""
    base_path = Path.cwd()
    
    init_wiki_structure(base_path, 'wiki')
    init_wiki_structure(base_path, 'personal')
    
    # 创建 raw 目录
    (base_path / 'raw' / 'assets').mkdir(parents=True, exist_ok=True)
    
    click.echo('✓ Wiki 和 Personal 目录结构已初始化')
```

- [ ] **Step 2: 修改 ingest 命令支持路由**

```python
# wiki_cli.py（修改 ingest 命令）
@cli.command()
@click.argument('target_or_file')
@click.argument('file', required=False)
def ingest(target_or_file, file):
    """导入文档到 wiki 或 personal
    
    用法：
      ingest <file>           → 导入到 wiki
      ingest personal <file>  → 导入到 personal
    """
    # 解析参数
    if file is None:
        # 单参数：默认 wiki
        target = 'wiki'
        source_path = target_or_file
    else:
        # 双参数：指定目标
        target = target_or_file
        source_path = file
    
    if target not in ['wiki', 'personal']:
        click.echo(f'错误: target 必须是 wiki 或 personal，收到: {target}', err=True)
        raise click.Abort()
    
    config = _load_config()
    llm = _create_llm(config)
    
    source_file = Path(source_path)
    if not source_file.exists():
        click.echo(f'错误: 文件不存在: {source_file}', err=True)
        raise click.Abort()
    
    wiki_dir = Path.cwd() / target
    index_file = wiki_dir / 'index.md'
    log_file = wiki_dir / 'log.md'
    
    result = ingest_document(source_file, wiki_dir, index_file, log_file, llm)
    
    click.echo(f'✓ 处理 {source_file.name}，创建 {len(result["pages"])} 个页面')
```

- [ ] **Step 3: 修改 query 命令支持自动路由**

```python
# wiki_cli.py（修改 query 命令）
from core.query import query_wiki_auto

@cli.command()
@click.argument('question')
def query(question):
    """查询 wiki（自动检测 wiki/personal）"""
    config = _load_config()
    llm = _create_llm(config)
    base_path = Path.cwd()
    
    result = query_wiki_auto(question, base_path, llm)
    click.echo(f"\n{result['answer']}\n")
    if result['sources']:
        click.echo("来源:")
        for source in result['sources']:
            click.echo(f"  - {source}")
```

- [ ] **Step 4: 修改 lint 命令支持双 wiki**

```python
# wiki_cli.py（修改 lint 命令）
from core.lint import lint_dual_wiki

@cli.command()
def lint():
    """检查 wiki 和 personal 健康状况"""
    base_path = Path.cwd()
    
    issues = lint_dual_wiki(base_path)
    if not issues:
        click.echo('✓ Wiki 和 Personal 健康状况良好')
        return
    
    click.echo(f'发现 {len(issues)} 个问题:\n')
    for issue in issues:
        click.echo(f'  {issue}')
```

- [ ] **Step 5: 测试 CLI 命令**

```bash
source venv/bin/activate
python wiki_cli.py --help
python wiki_cli.py init
python wiki_cli.py lint
```

Expected: 命令正常执行，显示帮助信息

- [ ] **Step 6: Commit**

```bash
git add wiki_cli.py
git commit -m "feat: update CLI to support dual wiki routing"
```

### Task 7: 创建 .claude/CLAUDE.md Schema

**Files:**
- Create: `.claude/CLAUDE.md`

- [ ] **Step 1: 创建 Schema 文档**

```markdown
# .claude/CLAUDE.md
# LLM Wiki Schema

This vault follows the LLM Wiki pattern: you maintain a persistent, structured knowledge base by incrementally
processing sources and building interconnected markdown pages.

## Architecture

- **raw/** - Immutable source documents (articles, papers, PDFs, images). You read from here but never modify.
- **raw/assets/** - Downloaded images and media files from web sources.
- **wiki/** - LLM-generated markdown files. 客观知识：外部资料、技术原理。
- **personal/** - LLM-generated markdown files. 主观知识：个人经历、反思、项目。与 wiki 完全同构但严格隔离。

## Knowledge Base Structure（同构设计）

### wiki/（客观知识）
- `index.md` - Catalog of all pages
- `log.md` - Chronological record of operations
- `sources/` - 外部文章、论文、教程
- `concepts/` - 技术原理、方法论
- `entities/` - 工具、人物、组织
- `comparisons/` - 技术对比分析
- `questions/` - 问答记录

### personal/（主观知识，完全同构）
- `index.md` - Catalog of all pages
- `log.md` - Chronological record of operations
- `sources/` - 个人经历记录、实践日志、项目记录
- `concepts/` - 个人方法论、经验总结、教训
- `entities/` - 我的项目、作品、工具
- `reflections/` - 深度反思、决策记录

## Core Operations

### Ingest（路由规则）
**命令**：
- `ingest <file>` → 默认路由到 wiki/（外部资料、技术文章、论文）
- `ingest personal <file>` → 路由到 personal/（个人经历、项目日志、反思）

**流程**（无讨论，直接执行）：
1. Read the source document from `raw/`
2. Create summary page in `{target}/sources/`
3. Update relevant pages in `{target}/concepts/` and `{target}/entities/`
4. Update `{target}/index.md`
5. Append entry to `{target}/log.md`
6. **Delete the source document from `raw/`** (cleanup after processing)
7. 一句话报告：处理了什么，创建了几个页面

### Query（默认隔离）
**路由规则**：
- 默认：只读 `wiki/index.md`（客观知识优先）
- 触发 personal：用户说"personal"/"我的"/"我之前"或第一人称问题
- 模糊情况：优先 wiki（保守策略）

**流程**：
1. Read `{target}/index.md` to find relevant pages
2. Read those pages
3. Synthesize answer with citations

### Lint（跨库检查 + 规模监控）
Check both wiki and personal health:
- Contradictions between pages (within each knowledge base)
- Orphan pages with no inbound links
- Missing cross-references
- **❌ wiki 引用 personal**（报错：客观知识不能依赖主观内容）
- **同名文件冲突**（wiki/concepts/xxx.md vs personal/concepts/xxx.md）
- **死链接**（personal 引用的 wiki 页面不存在）

**规模监控**（自动检查 index.md 大小）：
- `wiki/index.md` 或 `personal/index.md` 超过 300 行 → ⚠️ 警告：建议分层 index
- 超过 500 行 → 🔴 严重：必须分层 index

## Cross-references（跨库引用规则）

- 同库引用：`[[page-name]]` 或 `[[sources/source-name]]`
- personal → wiki：✅ 允许（`[[concepts/xxx]]` 默认指向 wiki）
- wiki → personal：❌ 禁止（客观知识不依赖主观）
- 明确跨库：`[[wiki/concepts/xxx]]` 或 `[[personal/concepts/xxx]]`

## Naming Conventions（避免冲突）

- wiki/concepts/ - 通用概念（如 prompt-caching.md）
- personal/concepts/ - 个人方法（加前缀，如 my-debugging-workflow.md）
- 避免同名文件，Lint 时检查冲突
```

- [ ] **Step 2: Commit**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: add LLM Wiki schema to .claude/CLAUDE.md"
```

### Task 8: 更新配置文件

**Files:**
- Modify: `config.yaml`

- [ ] **Step 1: 更新配置支持双 wiki**

```yaml
# config.yaml（完全替换）
llm:
  provider: claude
  model: claude-opus-4-6
  api_key: ${ANTHROPIC_API_KEY}

paths:
  wiki: ./wiki
  personal: ./personal
  raw: ./raw

search:
  tool: ripgrep
  max_results: 10

lint:
  index_warning_lines: 300
  index_critical_lines: 500
```

- [ ] **Step 2: Commit**

```bash
git add config.yaml
git commit -m "config: update for dual wiki support"
```

---

### Task 9: 更新 README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新 README 文档**

```markdown
# README.md（完全替换）
# LLM Wiki 双知识库系统

基于 [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的 LLM Wiki 系统。

## 架构

双知识库设计：
- **wiki/** - 客观知识（外部资料、技术原理）
- **personal/** - 主观知识（个人经历、项目、反思）

两个库完全同构但严格隔离，避免知识污染。

## 安装

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 初始化

```bash
source venv/bin/activate
python wiki_cli.py init
```

## 使用

### 导入文档

```bash
# 导入到 wiki（默认）
python wiki_cli.py ingest article.md

# 导入到 personal
python wiki_cli.py ingest personal my-project-log.md
```

### 查询知识

```bash
# 查客观知识（默认）
python wiki_cli.py query "What is Transformer?"

# 查个人经验（自动检测）
python wiki_cli.py query "我之前怎么调试的？"
```

### 健康检查

```bash
python wiki_cli.py lint
```

## 目录结构

```
HPC_VAULT/
├── .claude/
│   └── CLAUDE.md          # Schema 定义
├── wiki/                  # 客观知识库
│   ├── index.md
│   ├── log.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   ├── comparisons/
│   └── questions/
├── personal/              # 主观知识库
│   ├── index.md
│   ├── log.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   └── reflections/
└── raw/                   # 待处理文档
    └── assets/
```

## 核心特性

1. **严格隔离**：wiki 和 personal 互不污染
2. **自动路由**：ingest 默认进 wiki，ingest personal 进 personal
3. **规模监控**：lint 自动检查 index 大小，提醒重构
4. **同构设计**：两个库结构完全一致
5. **交叉引用**：personal 可以引用 wiki，反之禁止

## 测试

```bash
source venv/bin/activate
python -m pytest tests/ -v
```
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README for dual wiki architecture"
```

---

## 完成检查

- [ ] 所有测试通过
- [ ] CLI 命令可用
- [ ] wiki/ 和 personal/ 目录已创建
- [ ] .claude/CLAUDE.md 已创建
- [ ] 文档已更新


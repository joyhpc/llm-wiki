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

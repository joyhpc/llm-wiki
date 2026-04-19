---
name: LLM Wiki Implementation
description: 基于 Karpathy gist 的 LLM Wiki 系统实现
type: design
---

# LLM Wiki 设计文档

## 概述

基于 https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f 实现 LLM Wiki 系统。

核心理念：LLM 维护结构化 markdown wiki，而非每次查询都做 RAG 检索。

## 架构

### 文件结构

```
raw/              # 原始文档（不可变）
raw/assets/       # 资源文件（图片等）
wiki/             # LLM 生成的 markdown 页面
index.md          # 内容目录
log.md            # 操作日志
schema.md         # 配置文件
```

### 三层架构

1. **Raw sources** - 不可变的原始文档
2. **Wiki layer** - LLM 生成和维护的 markdown 文件
3. **Schema** - 定义 wiki 结构和工作流的配置

## 核心功能

### 1. Ingest（导入）

**流程**：
1. 读取原始文档
2. LLM 提取关键信息
3. 查找相关 wiki 页面
4. 更新现有页面或创建新页面
5. 维护交叉引用
6. 更新 index.md 和 log.md

**支持格式**：
- Markdown
- 纯文本
- PDF（基础解析）

### 2. Query（查询）

**流程**：
1. 接收用户问题
2. 搜索相关 wiki 页面
3. LLM 合成答案
4. 返回带引用的回答

### 3. Search（搜索）

**实现**：
- 使用 ripgrep 全文搜索
- 支持文件名、标题、标签过滤
- 返回相关页面片段

### 4. Lint（健康检查）

**检查项**：
- 页面间的矛盾
- 过时的声明
- 孤立页面（无引用）
- 损坏的链接

## 技术实现

### LLM 集成

**支持的 Provider**：
- Claude API（anthropic SDK）
- Ollama（本地 LLM）

**配置方式**：
```yaml
llm:
  provider: claude  # 或 ollama
  model: claude-opus-4-6
  api_key: ${ANTHROPIC_API_KEY}
```

### CLI 命令

```bash
wiki init                    # 初始化目录结构
wiki ingest <file>           # 导入文档
wiki query <question>        # 查询知识库
wiki search <keyword>        # 搜索内容
wiki lint                    # 健康检查
```

### 特殊文件格式

**index.md**：
- 按分类组织内容
- 包含页面链接和摘要
- LLM 自动维护

**log.md**：
- 时间序列记录
- 格式：`## [YYYY-MM-DD] operation | Description`
- 仅追加，不修改历史

**schema.md**：
- 定义 wiki 的分类体系
- 定义页面模板
- 定义工作流规则

## 数据流

### Ingest 数据流

```
原始文档 
  → LLM 提取信息 
  → 查找相关页面 
  → 更新/创建页面 
  → 更新索引 
  → 记录日志
```

### Query 数据流

```
用户问题 
  → 搜索相关页面 
  → LLM 合成答案 
  → 返回带引用的回答
```

## 实现细节

### 目录结构

```
llm-wiki/
├── wiki_cli.py           # CLI 入口
├── core/
│   ├── llm.py           # LLM 抽象层
│   ├── ingest.py        # 导入逻辑
│   ├── query.py         # 查询逻辑
│   ├── search.py        # 搜索逻辑
│   └── lint.py          # 健康检查
├── utils/
│   ├── parser.py        # 文档解析
│   └── file_ops.py      # 文件操作
├── config.yaml          # 配置文件
└── requirements.txt     # 依赖
```

### 依赖

```
anthropic          # Claude API
ollama             # 本地 LLM
click              # CLI 框架
pyyaml             # 配置解析
pypdf              # PDF 解析
```

### 配置文件示例

```yaml
llm:
  provider: claude
  model: claude-opus-4-6
  api_key: ${ANTHROPIC_API_KEY}
  
paths:
  raw: ./raw
  wiki: ./wiki
  index: ./index.md
  log: ./log.md
  schema: ./schema.md

search:
  tool: ripgrep
  max_results: 10
```

## 错误处理

- LLM API 失败：重试 3 次，指数退避
- 文件解析失败：记录错误，跳过该文件
- 搜索无结果：返回空列表，不报错

## 测试策略

- 单元测试：各模块独立测试
- 集成测试：完整 ingest/query 流程
- 手动测试：实际文档导入和查询

## 未来扩展

- BM25 + 向量搜索（替代 ripgrep）
- Web UI（FastAPI + React）
- 多用户支持
- 版本控制（wiki 页面历史）

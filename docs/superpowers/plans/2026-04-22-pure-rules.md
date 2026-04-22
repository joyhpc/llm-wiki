# Karpathy LLM Wiki - 纯规则驱动

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建 CLAUDE.md schema，定义 wiki 维护规则，无需任何代码

**Architecture:** 
- 所有行为由 `~/my-wiki/CLAUDE.md` 定义
- Claude 读取规则 → 直接操作文件
- 无需 Python 工具函数，无需 CLI

**Tech Stack:** 纯 markdown + Claude 原生能力（Read/Write/Edit）

---

## 唯一任务：创建 CLAUDE.md

**Files:**
- Create: `~/my-wiki/CLAUDE.md`

### Step 1: 创建 wiki 目录结构

```bash
mkdir -p ~/my-wiki/raw/assets
mkdir -p ~/my-wiki/wiki/{sources,concepts,entities}
touch ~/my-wiki/wiki/index.md
touch ~/my-wiki/wiki/log.md
```

### Step 2: 编写 CLAUDE.md schema

```markdown
# LLM Wiki Schema

你是这个 wiki 的维护者。遵循以下规则维护知识库。

## 目录结构

```
~/my-wiki/
├── raw/              # 源文档（人类策展，只读）
│   ├── assets/       # 图片等资源
│   └── *.pdf/txt/md  # 源文件
├── wiki/             # Wiki 页面（你维护）
│   ├── index.md      # 索引（必须维护）
│   ├── log.md        # 操作日志（必须记录）
│   ├── sources/      # 源文档摘要
│   ├── concepts/     # 概念页面
│   └── entities/     # 实体页面
└── CLAUDE.md         # 本文件
```

## Ingest 工作流

当用户说"摄入 X"或"处理 raw/X"时：

### 1. 读取现有状态

读取 `wiki/index.md`，提取所有现有页面：
- 查找所有 `[title](path)` 格式的链接
- 记录页面标题和路径

### 2. 分析新源

读取源文件，识别：
- **需要更新的现有页面**：新信息可以集成到哪些页面
- **需要创建的新页面**：哪些概念/实体需要独立页面
- **矛盾信息**：是否与现有内容冲突

输出分析结果：
```
分析结果：
UPDATE: concepts/transformer.md
  原因：新源提供了 attention 机制的详细信息

CREATE: concepts/attention-mechanism.md
  原因：attention 是核心概念，需要独立页面

CONTRADICTION: concepts/model-size.md
  原因：新源称 175B 参数，现有页面称 100B
```

### 3. 更新现有页面

对每个需要更新的页面：

1. 读取当前内容
2. 在适当位置集成新信息
3. 如果有矛盾，添加 `## Contradictions` 章节：
   ```markdown
   ## Contradictions
   
   ⚠️ Source A (paper.pdf) claims 100B parameters
   ⚠️ Source B (new-paper.pdf) claims 175B parameters
   ```
4. 更新交叉引用 `[[page-name]]`
5. 保存文件

### 4. 创建新页面

对每个新页面：

1. 确定目录（sources/concepts/entities）
2. 生成完整内容（见"页面格式"）
3. 添加交叉引用
4. 保存文件

### 5. 更新 index.md

在适当分类下添加/更新条目：
```markdown
## Concepts
- [Transformer](concepts/transformer.md) - Neural network architecture
- [Attention Mechanism](concepts/attention-mechanism.md) - Focusing mechanism ← 新增
```

### 6. 记录到 log.md

追加条目：
```markdown
## [2026-04-22 10:30] ingest | paper.pdf

Updated: 1 page
- concepts/transformer.md

Created: 1 page
- concepts/attention-mechanism.md

Contradictions found: 0
```

## Query 工作流

当用户提问时：

### 1. 读取 index.md

读取完整的 `wiki/index.md`

### 2. 识别相关页面

基于问题和 index 内容，列出最相关的 3-5 个页面路径

### 3. 读取页面内容

读取识别出的页面完整内容

### 4. 生成答案

基于页面内容回答，格式：
```markdown
[答案内容]

来源：
- concepts/transformer.md
- concepts/attention-mechanism.md
```

## 页面格式

### 概念页面 (concepts/)

```markdown
# Concept Name

简短定义（1-2 句）。

## 详细说明

深入解释。

## 相关概念

- [[related-concept-1]]
- [[related-concept-2]]

## Contradictions

⚠️ Source A claims X, Source B claims Y

## 来源

- [[source-1]]
- [[source-2]]
```

### 源摘要页面 (sources/)

```markdown
# Document Title

## 摘要

文档核心内容。

## 关键概念

- [[concept-1]]
- [[concept-2]]

## 元数据

- 类型：paper/article/book
- 日期：YYYY-MM-DD
- 作者：Name
```

### 实体页面 (entities/)

```markdown
# Entity Name

## 描述

实体说明。

## 相关概念

- [[concept-1]]

## 来源

- [[source-1]]
```

## 维护规则

1. **更新优先于创建**：能集成到现有页面就不创建新页面
2. **明确标记矛盾**：不删除冲突信息，用 ⚠️ 标记
3. **保持交叉引用**：使用 `[[page-name]]` 链接
4. **简洁索引**：index.md 每条一行，含简短描述
5. **时间戳日志**：log.md 每条以 `## [YYYY-MM-DD HH:MM]` 开头

## 操作示例

### 示例 1：首次摄入

```
用户：摄入 raw/transformer-paper.pdf

你的操作：
1. 读取 wiki/index.md（空的）
2. 分析论文，识别概念：Transformer, Attention, Encoder, Decoder
3. 创建 4 个概念页面 + 1 个源摘要页面
4. 更新 index.md 添加 5 个条目
5. 记录到 log.md

输出：
✓ 创建 5 个页面
  - sources/transformer-paper.md
  - concepts/transformer.md
  - concepts/attention.md
  - concepts/encoder.md
  - concepts/decoder.md
```

### 示例 2：更新现有内容

```
用户：摄入 raw/attention-details.pdf

你的操作：
1. 读取 wiki/index.md，发现已有 concepts/attention.md
2. 分析新论文，发现补充了 attention 的数学细节
3. 更新 concepts/attention.md，添加"数学原理"章节
4. 创建 sources/attention-details.md
5. 更新 index.md（源摘要）
6. 记录到 log.md

输出：
✓ 更新 1 个页面
  - concepts/attention.md
✓ 创建 1 个页面
  - sources/attention-details.md
```

### 示例 3：发现矛盾

```
用户：摄入 raw/gpt3-paper.pdf

你的操作：
1. 读取 wiki/index.md，发现已有 concepts/gpt3.md
2. 分析新论文，发现参数量与现有页面不一致
3. 更新 concepts/gpt3.md，添加 Contradictions 章节：
   ⚠️ Original source claims 175B, new paper claims 176B
4. 创建 sources/gpt3-paper.md
5. 更新 index.md 和 log.md

输出：
✓ 更新 1 个页面（发现矛盾）
  - concepts/gpt3.md
✓ 创建 1 个页面
  - sources/gpt3-paper.md
```

### 示例 4：查询

```
用户：transformer 是什么？

你的操作：
1. 读取 wiki/index.md
2. 识别相关页面：concepts/transformer.md, concepts/attention.md
3. 读取这 2 个页面
4. 生成答案

输出：
Transformer 是一种神经网络架构，使用 attention 机制处理序列数据...

来源：
- concepts/transformer.md
- concepts/attention.md
```

## 重要提醒

- **不要编造内容**：只基于源文档提取信息
- **保持一致性**：页面间的交叉引用必须准确
- **透明操作**：每次操作都解释你在做什么
- **遵循格式**：严格按照页面格式模板
```

### Step 3: 初始化 index.md

```markdown
# Wiki Index

## Sources

## Concepts

## Entities
```

### Step 4: 初始化 log.md

```markdown
# Wiki Log

操作历史记录。
```

### Step 5: 验证

检查文件结构：
```bash
tree ~/my-wiki/
```

Expected:
```
~/my-wiki/
├── CLAUDE.md
├── raw/
│   └── assets/
└── wiki/
    ├── index.md
    ├── log.md
    ├── sources/
    ├── concepts/
    └── entities/
```

### Step 6: 测试规则

放一个测试文件到 `raw/`，告诉 Claude："摄入 raw/test.txt"

Expected: Claude 读取 CLAUDE.md → 执行工作流 → 更新 wiki

---

## 完成标准

- [x] `~/my-wiki/CLAUDE.md` 存在且完整
- [x] 定义了 Ingest 工作流（6 个步骤）
- [x] 定义了 Query 工作流（4 个步骤）
- [x] 定义了页面格式（3 种类型）
- [x] 定义了维护规则（5 条）
- [x] 包含操作示例（4 个场景）
- [x] 目录结构已创建
- [x] index.md 和 log.md 已初始化

---

## 使用方式

**摄入：**
```
用户：摄入 raw/paper.pdf
Claude：[读取 CLAUDE.md → 执行 Ingest 工作流]
```

**查询：**
```
用户：查询 transformer
Claude：[读取 CLAUDE.md → 执行 Query 工作流]
```

**维护：**
```
用户：检查 wiki 健康状态
Claude：[读取 CLAUDE.md → 检查矛盾、孤立页面等]
```

---

## 核心优势

1. **零代码**：只有 CLAUDE.md 规则文件
2. **完全透明**：所有操作都是文件读写
3. **易于调整**：修改 CLAUDE.md 即可改变行为
4. **符合 Karpathy 理念**：Schema 驱动，LLM 维护

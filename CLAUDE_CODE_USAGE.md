# 在 Claude Code 中使用 LLM Wiki

## 优势

在 Claude Code 环境中使用 LLM Wiki 有以下优势：
- ✅ **无需 API Key** - 自动复用当前 Claude Code 会话
- ✅ **无额外费用** - 使用你已有的 Claude Code 订阅
- ✅ **无缝集成** - 直接在开发环境中管理知识

## 完整流程

### 1. 安装 LLM Wiki

```bash
# 在 Claude Code 终端中执行
cd ~/projects
git clone https://github.com/your-username/llm-wiki.git
cd llm-wiki
pip install -e .
```

### 2. 创建工作目录

```bash
# 创建你的知识库目录
mkdir ~/my-research-wiki
cd ~/my-research-wiki

# 初始化结构
python -m llm_wiki.cli init
```

这会创建：
```
~/my-research-wiki/
├── wiki/          # 客观知识
├── personal/      # 主观知识
└── raw/           # 待处理文档
```

### 3. 配置（Claude Code 环境）

创建 `config.yaml`：
```yaml
llm:
  provider: auto  # 自动检测 Claude Code 环境
  # 无需填写 api_key！
  model: claude-sonnet-4-20250514
```

**注意**：`provider: auto` 会自动检测到 Claude Code 环境，无需配置 API key。

### 4. 使用流程

#### 场景 1：导入论文笔记

```bash
# 1. 将论文 PDF 放入 raw/
cp ~/Downloads/transformer-paper.pdf raw/

# 2. 导入到 wiki（客观知识）
python -m llm_wiki.cli ingest raw/transformer-paper.pdf

# 3. 查看生成的页面
ls wiki/sources/
ls wiki/concepts/
```

#### 场景 2：记录项目经验

```bash
# 1. 创建项目笔记
cat > raw/my-project-notes.md << 'EOF'
# 项目 X 调试记录

今天遇到了内存泄漏问题，最后发现是...
EOF

# 2. 导入到 personal（主观知识）
python -m llm_wiki.cli ingest personal raw/my-project-notes.md

# 3. 查看
ls personal/reflections/
```

#### 场景 3：查询知识

```bash
# 查询客观知识（自动路由到 wiki）
python -m llm_wiki.cli query "What is the Transformer architecture?"

# 查询个人经验（自动路由到 personal）
python -m llm_wiki.cli query "我之前怎么解决内存泄漏的？"

# 搜索关键词
python -m llm_wiki.cli search "attention mechanism"
```

#### 场景 4：整理和合并

```bash
# 查找相似页面
python -m llm_wiki.cli merge wiki concepts --threshold 0.8

# 健康检查
python -m llm_wiki.cli lint

# 查看引用关系
python -m llm_wiki.cli references wiki transformer.md
```

### 5. 在 Claude Code 中的典型工作流

**研究论文时：**
```bash
# 1. 下载论文到 raw/
# 2. 导入
python -m llm_wiki.cli ingest raw/paper.pdf

# 3. 在 Claude Code 中继续对话
# "帮我总结一下刚才导入的论文"
# Claude Code 可以访问 wiki/ 中生成的页面
```

**写代码时：**
```bash
# 1. 记录设计决策
cat > raw/design-decision.md << 'EOF'
# API 设计决策

选择 REST 而不是 GraphQL，因为...
EOF

python -m llm_wiki.cli ingest personal raw/design-decision.md

# 2. 后续查询
python -m llm_wiki.cli query "为什么我们选择 REST？"
```

**学习新技术时：**
```bash
# 1. 导入文档
python -m llm_wiki.cli ingest raw/react-docs.md

# 2. 边学边问
python -m llm_wiki.cli query "React hooks 的最佳实践是什么？"

# 3. 记录心得
# 写到 personal/reflections/
```

## 工作流程图

```
Claude Code 会话
    ↓
下载/创建文档 → raw/
    ↓
python -m llm_wiki.cli ingest
    ↓
LLM 分析（复用 Claude Code 会话）
    ↓
分类存储到 wiki/ 或 personal/
    ↓
python -m llm_wiki.cli query
    ↓
LLM 综合回答（复用 Claude Code 会话）
    ↓
继续在 Claude Code 中对话
```

## 与 Claude Code 的集成优势

1. **无缝对话**
   - 导入文档后，可以直接在 Claude Code 中问："刚才导入的论文讲了什么？"
   - Claude Code 可以读取 wiki/ 中的页面

2. **零配置**
   - 无需管理 API key
   - 自动检测环境

3. **统一上下文**
   - 代码和知识在同一个环境
   - 可以直接引用 wiki 中的概念

## 注意事项

### 当前限制

由于 LLM Wiki 的 Claude Code Provider 还在开发中，目前需要：

**临时方案**：使用独立 API key
```yaml
llm:
  provider: claude  # 暂时使用 claude 模式
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-20250514
```

设置环境变量：
```bash
export ANTHROPIC_API_KEY="your-key"
```

**未来版本**：将完全支持 Claude Code 环境，无需 API key。

## 最佳实践

1. **分离客观和主观**
   - 论文、文档 → wiki
   - 个人想法、项目经验 → personal

2. **定期整理**
   ```bash
   python -m llm_wiki.cli lint
   python -m llm_wiki.cli merge wiki concepts
   ```

3. **备份数据**
   ```bash
   tar -czf wiki-backup.tar.gz wiki/ personal/
   ```

4. **版本控制**
   ```bash
   cd ~/my-research-wiki
   git init
   git add wiki/ personal/
   git commit -m "knowledge snapshot"
   ```

## 示例：完整研究流程

```bash
# 1. 初始化
mkdir ~/ai-research && cd ~/ai-research
python -m llm_wiki.cli init

# 2. 导入论文
python -m llm_wiki.cli ingest raw/attention-is-all-you-need.pdf
python -m llm_wiki.cli ingest raw/bert-paper.pdf

# 3. 查询对比
python -m llm_wiki.cli query "Transformer 和 BERT 的区别是什么？"

# 4. 记录实验
cat > raw/experiment-log.md << 'EOF'
# 实验：微调 BERT

数据集：1000条
学习率：2e-5
结果：准确率 92%
EOF

python -m llm_wiki.cli ingest personal raw/experiment-log.md

# 5. 后续查询
python -m llm_wiki.cli query "我上次微调 BERT 用的什么参数？"
```

## 获取帮助

```bash
python -m llm_wiki.cli --help
python -m llm_wiki.cli ingest --help
python -m llm_wiki.cli query --help
```

---

有问题随时在 Claude Code 中问我！

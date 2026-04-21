# LLM Wiki 使用指南

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/llm-wiki.git
cd llm-wiki
```

### 2. 安装

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e .
```

### 3. 初始化工作目录

```bash
# 创建你的 wiki 目录
mkdir ~/my-wiki
cd ~/my-wiki

# 初始化结构
python -m llm_wiki.cli init
```

### 4. 配置 LLM

```bash
# 复制配置模板
cp /path/to/llm-wiki/config.yaml.example config.yaml

# 编辑 config.yaml
# 将 api_key: ${ANTHROPIC_API_KEY} 改为你的实际 API key
# 或者设置环境变量: export ANTHROPIC_API_KEY="your-key"
```

配置示例：
```yaml
llm:
  provider: auto  # 自动检测环境
  api_key: sk-ant-xxxxx  # 或使用 ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-20250514
```

### 5. 开始使用

```bash
# 导入文档到 wiki（客观知识）
python -m llm_wiki.cli ingest article.md

# 导入到 personal（主观知识）
python -m llm_wiki.cli ingest personal my-notes.md

# 查询
python -m llm_wiki.cli query "What is Transformer?"

# 搜索
python -m llm_wiki.cli search "keyword"

# 健康检查
python -m llm_wiki.cli lint

# 查找相似页面并合并
python -m llm_wiki.cli merge wiki concepts --threshold 0.8
```

## 核心概念

### 双知识库
- **wiki/** - 客观知识（论文、技术文档、外部资料）
- **personal/** - 主观知识（个人想法、项目经验、反思）

### 分类结构
- **sources/** - 原始资料
- **concepts/** - 概念和原理
- **entities/** - 实体（人物、工具、框架）
- **comparisons/** - 对比分析
- **questions/** - 问答
- **reflections/** - 个人反思（仅 personal）

## 常见问题

### Q: 如何获取 Anthropic API key？
访问 https://console.anthropic.com/ 注册并创建 API key

### Q: 可以使用本地 LLM 吗？
可以，配置 `provider: ollama` 并安装 Ollama

### Q: 如何备份数据？
直接备份 wiki/ 和 personal/ 目录即可

### Q: 支持哪些文档格式？
Markdown (.md) 和 PDF (.pdf)

## 更多信息

- [完整文档](README.md)
- [架构设计](docs/superpowers/specs/2026-04-21-opensource-release-design.md)
- [示例项目](examples/research-notes/)

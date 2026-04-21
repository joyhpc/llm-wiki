# LLM Wiki v0.1.0 Release Notes

## 🎉 首次发布

LLM Wiki 是一个基于 LLM 的知识管理系统，灵感来自 [Andrej Karpathy 的 gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

## ✨ 核心特性

### 双知识库架构
- **wiki/** - 客观知识（外部资料、技术原理）
- **personal/** - 主观知识（个人经历、项目反思）
- 严格隔离，避免知识污染

### LLM 驱动
- 自动解析文档内容
- 智能分类存储（sources/concepts/entities/comparisons/questions）
- 语义查询和路由
- 页面合并优化（并查集算法）

### 环境自适应
- 自动检测 AI Assistant/AI Environment 环境
- 独立运行时支持 Claude API 和 Ollama
- 无需重复配置 API key

### 完整功能
- ✅ 文档导入（ingest）
- ✅ 智能查询（query）
- ✅ 页面合并（merge）
- ✅ 引用追踪（references）
- ✅ 归档管理（archive）
- ✅ 健康检查（lint）
- ✅ 全文搜索（search）

## 📦 安装

```bash
git clone https://github.com/your-username/llm-wiki.git
cd llm-wiki
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## 🚀 快速开始

```bash
# 初始化
mkdir ~/my-wiki && cd ~/my-wiki
python -m llm_wiki.cli init

# 配置（如果独立运行）
cp /path/to/config.yaml.example config.yaml
# 编辑 config.yaml，填入 API key

# 使用
python -m llm_wiki.cli ingest article.md
python -m llm_wiki.cli query "What is Transformer?"
```

## 📚 文档

- [README](README.md) - 快速开始
- [架构设计](docs/superpowers/specs/2026-04-21-opensource-release-design.md)
- [示例项目](examples/research-notes/)

## 🙏 致谢

基于 Andrej Karpathy 的 [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## 📝 完整变更日志

见 [CHANGELOG.md](CHANGELOG.md)

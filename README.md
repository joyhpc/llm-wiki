# LLM Wiki

基于 [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的 LLM 知识管理系统。

## 特性

- **双知识库设计** - wiki（客观知识）和 personal（主观知识）严格隔离
- **LLM 驱动** - 自动解析文档、智能查询、语义合并
- **分类索引** - sources/concepts/entities/comparisons/questions 结构化存储
- **智能路由** - 自动检测查询目标（wiki vs personal）
- **页面合并** - 使用并查集优化，自动归档旧版本
- **引用追踪** - 级联更新通知
- **环境自适应** - 自动检测 Claude Code/Codex 环境，无需配置 API key

## 快速开始

### 安装

```bash
# 1. Clone 项目
git clone https://github.com/your-username/llm-wiki.git
cd llm-wiki

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装
pip install -e .
```

### 初始化

```bash
# 创建工作目录
mkdir ~/my-wiki
cd ~/my-wiki

# 初始化 wiki 结构
python -m llm_wiki.cli init

# 配置 LLM（如果独立运行）
cp /path/to/llm-wiki/config.yaml.example config.yaml
# 编辑 config.yaml，填入 API key
```

### 基本使用

```bash
# 导入文档到 wiki（客观知识）
python -m llm_wiki.cli ingest article.md

# 导入到 personal（主观知识）
python -m llm_wiki.cli ingest personal my-notes.md

# 查询
python -m llm_wiki.cli query "What is Transformer?"

# 查找并合并相似页面
python -m llm_wiki.cli merge wiki concepts --threshold 0.8

# 健康检查
python -m llm_wiki.cli lint
```

## 文档

- [架构设计](docs/architecture.md) - 双知识库设计、分类索引结构
- [API 参考](docs/api.md) - 核心模块说明
- [使用案例](docs/use-cases.md) - 学术研究、技术文档、个人知识库
- [故障排查](docs/troubleshooting.md) - 常见问题解决

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 见 [LICENSE](LICENSE)

## 致谢

基于 Andrej Karpathy 的 [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)


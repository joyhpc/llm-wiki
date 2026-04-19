# LLM Wiki

基于 [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的 LLM Wiki 系统。

## 特性

- LLM 维护结构化 markdown wiki
- 支持 Claude API 和 Ollama
- 文档导入、查询、搜索
- Wiki 健康检查

## 安装

```bash
pip install -r requirements.txt
```

## 配置

复制 `config.yaml` 并配置：

```yaml
llm:
  provider: claude  # 或 ollama
  model: claude-opus-4-6
  api_key: ${ANTHROPIC_API_KEY}
```

## 使用

```bash
# 初始化
python3 wiki_cli.py init

# 导入文档
python3 wiki_cli.py ingest path/to/document.md

# 查询
python3 wiki_cli.py query "What is Python?"

# 搜索
python3 wiki_cli.py search "keyword"

# 健康检查
python3 wiki_cli.py lint
```

## 架构

```
raw/              # 原始文档（不可变）
wiki/             # LLM 生成的 wiki 页面
index.md          # 内容目录
log.md            # 操作日志
schema.md         # Wiki 结构配置
```

## 测试

```bash
python3 -m pytest tests/ -v
```

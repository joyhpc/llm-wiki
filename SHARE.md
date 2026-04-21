# 给朋友的使用说明

嘿！这是一个基于 LLM 的知识管理系统，可以帮你整理笔记、论文和文档。

## 三步开始

**1. 安装**
```bash
git clone https://github.com/your-username/llm-wiki.git
cd llm-wiki
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**2. 初始化**
```bash
mkdir ~/my-wiki && cd ~/my-wiki
python -m llm_wiki.cli init
cp /path/to/llm-wiki/config.yaml.example config.yaml
```

编辑 `config.yaml`，填入你的 Anthropic API key：
```yaml
llm:
  provider: auto
  api_key: sk-ant-你的密钥
  model: claude-sonnet-4-20250514
```

**3. 使用**
```bash
# 导入文档
python -m llm_wiki.cli ingest your-document.md

# 查询
python -m llm_wiki.cli query "你的问题"
```

## 核心功能

- **wiki/** - 存放客观知识（论文、技术文档）
- **personal/** - 存放主观知识（个人想法、项目笔记）
- 自动分类、智能查询、页面合并

## 获取 API Key

访问 https://console.anthropic.com/ 注册并创建 API key

## 完整文档

见 [QUICKSTART.md](QUICKSTART.md) 和 [README.md](README.md)

---

有问题随时问我！

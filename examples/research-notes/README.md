# Research Notes Example

这是一个学术研究笔记管理的示例项目。

## 场景

管理学术论文阅读笔记、研究想法和实验记录。

## 使用步骤

1. 初始化 wiki 结构：
```bash
cd examples/research-notes
python -m llm_wiki.cli init
```

2. 配置 LLM（如果独立运行）：
```bash
cp ../../config.yaml.example config.yaml
# 编辑 config.yaml，填入 API key
```

3. 导入论文笔记：
```bash
# 将论文 PDF 或笔记放入 raw/ 目录
python -m llm_wiki.cli ingest raw/paper1.pdf
```

4. 查询知识：
```bash
python -m llm_wiki.cli query "What is the main contribution of this paper?"
```

## 目录结构

```
research-notes/
├── wiki/              # 论文内容、概念、方法
├── personal/          # 个人想法、实验记录
├── raw/              # 待处理的论文和笔记
└── config.yaml       # 配置文件
```

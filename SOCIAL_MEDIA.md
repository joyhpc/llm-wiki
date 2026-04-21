# 朋友圈文案

## 版本 1：技术向

刚做了个基于 LLM 的知识管理系统 📚

灵感来自 Karpathy 的 gist，核心特性：
• 双知识库设计（客观/主观严格隔离）
• LLM 自动分类、智能查询、语义合并
• 支持 AI Assistant 环境，无需配置 API key
• 标准 Python 包，pip 一键安装

适合管理论文笔记、技术文档、项目经验。

开源了，需要的自取 👇
[GitHub 链接]

---

## 版本 2：简洁向

做了个 LLM 知识管理工具 🛠️

扔进去论文/文档，自动整理分类，随时查询。
支持 AI Assistant，零配置。

开源，需要的拿走 👇
[GitHub 链接]

---

## 版本 3：场景向

读论文太多记不住？项目经验找不到？

做了个 LLM Wiki 解决这个问题：
• 自动提取概念、实体、对比
• 智能查询，秒找答案
• 客观知识和主观想法分开存

已开源，Python 写的，很好用 👇
[GitHub 链接]

---

## 版本 4：极简向

开源了一个 LLM 知识管理系统

论文笔记、技术文档、项目经验都能管
基于 Claude，自动整理，智能查询

[GitHub 链接]

---

## 版本 5：Geek 向

```python
# 基于 Karpathy gist 的 LLM Wiki
# 双知识库 + 自动分类 + 语义查询

pip install -e llm-wiki
llm-wiki init
llm-wiki ingest paper.pdf
llm-wiki query "问题"

# 开源了，star 一下 ⭐
```

[GitHub 链接]

---

## 配图建议

1. **架构图**：展示 wiki/personal 双知识库结构
2. **终端截图**：展示 CLI 命令和输出
3. **目录树**：展示自动生成的分类结构
4. **对比图**：导入前后的对比

---

## Hashtags

#开源项目 #LLM #知识管理 #Python #Claude #AI工具 #效率工具 #笔记管理

---

## 评论区预设回复

**Q: 需要 API key 吗？**
A: 独立运行需要 Anthropic API key，在 AI Assistant 中用可以零配置

**Q: 支持哪些文档格式？**
A: 目前支持 Markdown 和 PDF，后续会加更多

**Q: 和 Notion/Obsidian 有什么区别？**
A: 这个是 LLM 驱动的，自动分类、智能查询，不用手动整理

**Q: 数据存在哪？**
A: 本地文件，Markdown 格式，随时备份和迁移

**Q: 怎么安装？**
A: 看 GitHub README，三步搞定：clone → pip install → init

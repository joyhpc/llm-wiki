# Contributing to LLM Wiki

感谢你对 LLM Wiki 的关注！

## 如何贡献

### 报告 Bug

在 [GitHub Issues](https://github.com/your-username/llm-wiki/issues) 中创建 issue，包含：
- 问题描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（Python 版本、操作系统）

### 提交功能请求

在 Issues 中描述：
- 功能用途
- 使用场景
- 可能的实现方案

### 提交代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码规范

- 使用 black 格式化代码
- 遵循 PEP 8
- 添加类型注解
- 编写测试覆盖新功能

### Commit 规范

使用 Conventional Commits：
- `feat:` - 新功能
- `fix:` - Bug 修复
- `docs:` - 文档更新
- `refactor:` - 代码重构
- `test:` - 测试相关

## 开发环境

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 代码格式化
black llm_wiki/ tests/

# 代码检查
flake8 llm_wiki/ tests/
```

## 问题？

有任何问题欢迎在 Issues 中提问。

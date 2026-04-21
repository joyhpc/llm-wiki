# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-21

### Added
- 双知识库架构（wiki/personal）
- 文档导入（ingest）支持分类存储
- 智能查询（query）自动路由
- 页面合并（merge）使用并查集优化
- 引用追踪（cascade）和归档（archive）
- 健康检查（lint）
- LLM provider 支持 auto 模式，自动检测 Claude Code/Codex 环境
- 标准 Python 包结构，支持 `pip install -e .`
- 配置模板 config.yaml.example

### Changed
- 重构为标准 Python 包（llm_wiki）
- 所有导入改为绝对路径

### Fixed
- 修复 index.md 和 log.md 被误判为名称冲突

[0.1.0]: https://github.com/your-username/llm-wiki/releases/tag/v0.1.0

---
name: LLM Wiki 开源发布设计
description: 生产级开源发布方案，包含项目结构、测试、CI/CD、文档、安全审查和性能优化
type: design
---

# LLM Wiki 开源发布设计

## 目标

将 LLM Wiki 系统打包为生产级开源项目，面向开发者用户，通过 GitHub Release 发布。

## 用户画像

- 技术水平：开发者（熟悉 Python、命令行、git）
- 安装方式：`git clone` + `pip install -e .`
- 使用场景：学术研究笔记、技术文档管理、个人知识库

## 核心设计决策

### 1. 数据目录：工作目录模式

用户在任意目录运行 `llm-wiki init` 创建独立 wiki 实例：

```
~/my-research-wiki/
├── wiki/          # 客观知识
├── personal/      # 主观知识
├── raw/           # 待处理文档
└── config.yaml    # 配置文件
```

支持多实例，类似 git 工作方式。

### 2. LLM Provider：Auto 模式

自动检测运行环境：
- AI Assistant/AI Environment：复用当前会话 LLM
- 独立运行：读取 config.yaml 中的 API key

配置示例：
```yaml
llm:
  provider: auto  # auto | claude | ollama
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-sonnet-4-20250514
```

### 3. 发布渠道

GitHub Release + 手动安装（不发布到 PyPI）

---

## 项目结构

```
llm-wiki/
├── llm_wiki/              # 重命名为标准包名
│   ├── __init__.py
│   ├── cli.py            # 从 wiki_cli.py 重构
│   ├── core/
│   │   ├── ingest.py
│   │   ├── query.py
│   │   ├── merge.py
│   │   ├── merge_optimizer.py
│   │   ├── cascade.py
│   │   ├── archive.py
│   │   ├── search.py
│   │   ├── lint.py
│   │   └── llm.py
│   └── utils/
│       └── init_wiki.py
├── tests/
│   ├── unit/
│   │   ├── test_ingest.py
│   │   ├── test_query.py
│   │   ├── test_merge.py
│   │   ├── test_merge_optimizer.py
│   │   ├── test_cascade.py
│   │   ├── test_archive.py
│   │   └── test_search.py
│   ├── integration/
│   │   ├── test_full_workflow.py
│   │   ├── test_dual_wiki.py
│   │   └── test_cli.py
│   └── fixtures/
│       ├── sample_docs/
│       └── mock_llm.py
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── troubleshooting.md
│   └── use-cases.md
├── examples/
│   ├── research-notes/
│   └── tech-docs/
├── .github/
│   └── workflows/
│       └── test.yml
├── setup.py
├── pyproject.toml
├── config.yaml.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

---

## 测试策略

### 测试覆盖目标

- 单元测试：Mock LLM，测试核心逻辑
- 集成测试：使用 fixture 文档，测试端到端流程
- 目标覆盖率：>80%

### 新增测试文件

**Unit Tests**
- `test_ingest.py` - 文档导入、分类存储
- `test_query.py` - 查询逻辑、路由
- `test_merge.py` - 页面合并、引用更新
- `test_merge_optimizer.py` - 并查集算法、合并顺序优化
- `test_cascade.py` - 引用追踪、级联更新
- `test_archive.py` - 归档功能、版本管理
- `test_search.py` - 搜索功能

**Integration Tests**
- `test_full_workflow.py` - init → ingest → query → merge 完整流程
- `test_dual_wiki.py` - wiki/personal 隔离验证
- `test_cli.py` - CLI 命令测试

**Fixtures**
- `sample_docs/` - 测试用文档（Markdown、PDF）
- `mock_llm.py` - Mock LLM 响应

---

## CI/CD 配置

### GitHub Actions

`.github/workflows/test.yml`：
- 触发条件：push、pull_request
- Python 版本矩阵：3.9, 3.10, 3.11, 3.12
- 步骤：安装依赖 → 运行测试 → 上传覆盖率报告
- 集成 Codecov

---

## 版本管理

### 语义化版本

- 0.1.0 - 首次发布
- 0.x.y - 功能迭代
- 1.0.0 - 生产就绪

### CHANGELOG.md 格式

```markdown
# Changelog

## [0.1.0] - 2026-04-21

### Added
- 双知识库架构（wiki/personal）
- 文档导入（ingest）支持分类存储
- 智能查询（query）自动路由
- 页面合并（merge）使用并查集优化
- 引用追踪（cascade）和归档（archive）
- 健康检查（lint）

### Changed
- LLM provider 支持 auto 模式，自动检测 AI Assistant/AI Environment 环境

### Fixed
- 修复 index.md 和 log.md 被误判为名称冲突
```

---

## 文档结构

### README.md

- 项目简介和特性
- 快速开始（安装、初始化、基本使用）
- 核心命令示例
- 文档链接
- 贡献指南和许可证

### docs/architecture.md

**内容**
- 双知识库设计（wiki vs personal）
- 分类索引结构（sources/concepts/entities/comparisons/questions）
- 核心流程（ingest/query/merge）
- LLM 集成（Provider 架构、auto 模式检测逻辑）

### docs/api.md

**内容**
- 核心模块 API 参考
- 每个模块的函数签名、参数说明、返回值
- 使用示例

**模块列表**
- `llm_wiki.core.ingest` - 文档导入
- `llm_wiki.core.query` - 查询
- `llm_wiki.core.merge` - 页面合并
- `llm_wiki.core.merge_optimizer` - 合并优化
- `llm_wiki.core.cascade` - 引用追踪
- `llm_wiki.core.archive` - 归档
- `llm_wiki.core.search` - 搜索
- `llm_wiki.core.lint` - 健康检查

### docs/troubleshooting.md

**内容**
- LLM 配置问题（API key、网络、模型支持）
- 文档导入问题（编码、格式、解析失败）
- 查询问题（未找到内容、路由错误）
- 每个问题的诊断步骤和解决方案

### docs/use-cases.md

**内容**
- 学术研究笔记（场景、工作流程、示例）
- 技术文档管理（场景、工作流程、示例）
- 个人知识库（场景、工作流程、示例）

---

## 示例项目

### examples/research-notes/

**目录结构**
```
research-notes/
├── README.md              # 场景说明、使用步骤
├── raw/
│   ├── paper1.pdf
│   └── notes.md
└── setup.sh               # 初始化脚本
```

**场景**：学术研究笔记管理

### examples/tech-docs/

**目录结构**
```
tech-docs/
├── README.md
├── raw/
│   ├── api-spec.md
│   └── architecture.md
└── setup.sh
```

**场景**：技术文档知识库

---

## 安全审查

### API Key 处理

- 支持环境变量 `${ANTHROPIC_API_KEY}`
- 配置文件权限检查（600）
- 日志中脱敏 API key

### 输入验证

- 文件路径验证（防止路径遍历）
- 文件大小限制
- 文件类型白名单

### 依赖安全

- 固定依赖版本范围
- 定期更新依赖
- GitHub Dependabot 自动检测漏洞

---

## 性能优化

### 大规模测试

- 测试 1000+ 页面场景
- 查询性能基准
- 合并算法复杂度验证

### 优化点

- 索引缓存（避免重复读取 index.md）
- 批量操作（merge 多个页面时减少 LLM 调用）
- 并发处理（多文档 ingest）

---

## 项目清理

### 需要清理

- 删除 `wiki/` 和 `personal/` 中的个人数据
- 删除 `raw/` 中的待处理文档
- 删除 `config.yaml`（保留 `config.yaml.example`）
- 清理 `.claude/` 目录（如果有敏感信息）

### 保留内容

- 代码和测试
- 文档和示例
- Git 历史（如果没有敏感信息）

### .gitignore 修正

当前 `.gitignore` 排除了所有 `.md` 文件，需要修正为：
```
__pycache__/
*.pyc
.pytest_cache/
config.yaml
.env
venv/

# 用户数据目录（仅在开发环境）
/wiki/
/personal/
/raw/
```

---

## 发布检查清单

### 代码质量
- [ ] 所有测试通过
- [ ] 测试覆盖率 >80%
- [ ] 代码风格一致（black/flake8）
- [ ] 类型注解完整

### 文档完整性
- [ ] README.md 完整
- [ ] 所有 docs/ 文档完成
- [ ] 示例项目可运行
- [ ] CONTRIBUTING.md 和 LICENSE 就位

### 安全检查
- [ ] 无硬编码 API key
- [ ] 输入验证完整
- [ ] 依赖无已知漏洞

### 功能验证
- [ ] 全流程测试（init → ingest → query → merge）
- [ ] 多环境测试（独立运行、AI Assistant、AI Environment）
- [ ] 性能测试通过

### 发布准备
- [ ] 个人数据已清理
- [ ] CHANGELOG.md 更新
- [ ] 版本号确定（0.1.0）
- [ ] GitHub Release 创建

---

## 实施计划

### 阶段 1：项目结构重构（1 天）
1. 重命名 `wiki_cli.py` → `llm_wiki/cli.py`
2. 调整包结构
3. 创建 `setup.py` 和 `pyproject.toml`
4. 修正 `.gitignore`
5. 创建 `config.yaml.example`

### 阶段 2：测试覆盖（2 天）
1. 编写单元测试（7 个新文件）
2. 编写集成测试（3 个文件）
3. 创建测试 fixtures
4. 运行测试，确保覆盖率 >80%

### 阶段 3：CI/CD 配置（0.5 天）
1. 创建 `.github/workflows/test.yml`
2. 配置 Codecov
3. 验证 CI 流程

### 阶段 4：文档编写（1.5 天）
1. 更新 README.md
2. 编写 docs/architecture.md
3. 编写 docs/api.md
4. 编写 docs/troubleshooting.md
5. 编写 docs/use-cases.md
6. 创建 CONTRIBUTING.md
7. 添加 LICENSE（MIT）

### 阶段 5：示例项目（0.5 天）
1. 创建 examples/research-notes/
2. 创建 examples/tech-docs/
3. 编写 setup.sh 脚本

### 阶段 6：安全与性能（0.5 天）
1. 实施 API key 安全处理
2. 添加输入验证
3. 运行大规模测试
4. 实施优化点

### 阶段 7：项目清理与发布（0.5 天）
1. 清理个人数据
2. 更新 CHANGELOG.md
3. 运行完整检查清单
4. 创建 GitHub Release v0.1.0

**总计：约 6.5 天**

---

## 风险与缓解

### 风险 1：测试覆盖率不足
- 缓解：优先测试核心流程，Mock LLM 降低复杂度

### 风险 2：文档编写耗时
- 缓解：使用模板，复用现有 README 内容

### 风险 3：性能问题
- 缓解：先发布 MVP，后续迭代优化

### 风险 4：多环境兼容性
- 缓解：CI 测试多个 Python 版本，手动测试 AI Assistant/AI Environment

---

## 成功标准

1. 开发者能在 5 分钟内完成安装和初始化
2. 所有核心功能（ingest/query/merge）正常工作
3. 文档清晰，新用户能独立上手
4. 测试覆盖率 >80%，CI 通过
5. 无已知安全漏洞


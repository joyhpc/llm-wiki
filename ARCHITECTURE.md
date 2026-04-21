# LLM Wiki 项目架构

## 目录结构

```
llm-wiki/
├── llm_wiki/                      # 核心包
│   ├── __init__.py               # 包初始化 (v0.1.0)
│   ├── cli.py                    # CLI 入口
│   ├── core/                     # 核心功能模块
│   │   ├── llm.py               # LLM Provider (Claude/Ollama/Auto)
│   │   ├── ingest.py            # 文档导入和分类
│   │   ├── query.py             # 智能查询
│   │   ├── router.py            # 查询路由 (wiki/personal)
│   │   ├── search.py            # 全文搜索
│   │   ├── merge.py             # 页面合并
│   │   ├── merge_optimizer.py  # 并查集优化
│   │   ├── cascade.py           # 引用追踪
│   │   ├── archive.py           # 归档管理
│   │   ├── lint.py              # 健康检查
│   │   └── index_manager.py     # 索引管理
│   └── utils/                    # 工具模块
│       ├── init_wiki.py         # Wiki 初始化
│       ├── parser.py            # 文档解析 (MD/PDF)
│       └── file_ops.py          # 文件操作
│
├── tests/                        # 测试
│   ├── test_llm.py
│   ├── test_router.py
│   ├── test_init_wiki.py
│   └── test_file_ops.py
│
├── examples/                     # 示例项目
│   └── research-notes/          # 学术研究笔记示例
│       ├── README.md
│       ├── setup.sh
│       └── raw/
│
├── docs/                         # 文档
│   └── superpowers/
│       ├── specs/               # 设计文档
│       │   ├── 2026-04-19-llm-wiki-design.md
│       │   ├── 2026-04-19-dual-wiki-refactor.md
│       │   └── 2026-04-21-opensource-release-design.md
│       └── plans/               # 实施计划
│           ├── 2026-04-19-llm-wiki.md
│           └── 2026-04-19-dual-wiki-refactor.md
│
├── setup.py                      # 安装配置
├── pyproject.toml               # 项目元数据
├── requirements.txt             # 依赖列表
├── config.yaml.example          # 配置模板
│
├── README.md                    # 项目说明
├── QUICKSTART.md                # 快速开始
├── SHARE.md                     # 分享指南
├── CONTRIBUTING.md              # 贡献指南
├── CHANGELOG.md                 # 变更日志
├── RELEASE_NOTES.md             # 发布说明
├── LICENSE                      # MIT 许可证
│
└── .gitignore                   # Git 忽略规则
```

## 运行时目录结构（用户工作目录）

```
~/my-wiki/                       # 用户工作目录
├── config.yaml                  # 用户配置
├── wiki/                        # 客观知识库
│   ├── index.md                # 总索引
│   ├── log.md                  # 操作日志
│   ├── sources/                # 原始资料
│   ├── concepts/               # 概念和原理
│   ├── entities/               # 实体（人物、工具）
│   ├── comparisons/            # 对比分析
│   └── questions/              # 问答
│
├── personal/                    # 主观知识库
│   ├── index.md
│   ├── log.md
│   ├── sources/
│   ├── concepts/
│   ├── entities/
│   └── reflections/            # 个人反思
│
└── raw/                         # 待处理文档
    └── assets/                 # 资源文件
```

## 核心模块架构

### 1. LLM Provider 层 (llm.py)
```
create_llm_provider()
    ├── auto 模式检测
    │   ├── AI Assistant 环境 → ClaudeCodeProvider
    │   ├── AI Environment 环境 → AIEnvironmentProvider
    │   └── 独立运行 → ClaudeProvider
    ├── claude 模式 → ClaudeProvider
    └── ollama 模式 → OllamaProvider
```

### 2. 文档处理流程
```
ingest.py
    ├── 解析文档 (parser.py)
    │   ├── Markdown
    │   └── PDF
    ├── LLM 分析
    │   ├── 提取概念
    │   ├── 识别实体
    │   └── 生成摘要
    ├── 分类存储
    │   ├── sources/
    │   ├── concepts/
    │   ├── entities/
    │   ├── comparisons/
    │   └── questions/
    └── 更新索引 (index_manager.py)
```

### 3. 查询流程
```
query.py
    ├── 路由检测 (router.py)
    │   ├── 客观问题 → wiki/
    │   └── 主观问题 → personal/
    ├── 搜索相关页面 (search.py)
    ├── LLM 综合回答
    └── 返回结果 + 引用
```

### 4. 页面合并流程
```
merge.py
    ├── 查找相似页面 (LLM 语义比较)
    ├── 优化合并顺序 (merge_optimizer.py)
    │   └── 并查集算法
    ├── 合并内容 (LLM)
    ├── 更新引用 (cascade.py)
    └── 归档旧版本 (archive.py)
```

## CLI 命令

```bash
llm-wiki init              # 初始化目录结构
llm-wiki ingest <file>     # 导入文档到 wiki
llm-wiki ingest personal <file>  # 导入到 personal
llm-wiki query "<question>"      # 查询
llm-wiki search "<keyword>"      # 搜索
llm-wiki merge <target> <category>  # 合并相似页面
llm-wiki references <target> <page>  # 查看引用
llm-wiki lint              # 健康检查
```

## 数据流

```
原始文档 (raw/)
    ↓
ingest (解析 + LLM 分析)
    ↓
分类存储 (wiki/ 或 personal/)
    ↓
索引更新 (index.md)
    ↓
查询/搜索 (LLM 综合)
    ↓
返回结果
```

## 技术栈

- **语言**: Python 3.9+
- **LLM**: Anthropic Claude API / Ollama
- **CLI**: Click
- **文档解析**: pypdf
- **配置**: PyYAML
- **测试**: pytest
- **打包**: setuptools

## 设计原则

1. **双知识库隔离** - wiki 和 personal 严格分离
2. **LLM 驱动** - 自动分类、智能查询、语义合并
3. **环境自适应** - 自动检测 AI Assistant/AI Environment/独立运行
4. **标准 Python 包** - 支持 pip 安装
5. **工作目录模式** - 类似 git，支持多实例

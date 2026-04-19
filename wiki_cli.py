#!/usr/bin/env python3
import click
import yaml
from pathlib import Path
from core.llm import ClaudeProvider, OllamaProvider
from core.ingest import ingest_document
from core.query import query_wiki_auto
from core.search import search_wiki
from core.lint import lint_dual_wiki
from utils.init_wiki import init_wiki_structure
import os

@click.group()
def cli():
    """LLM Wiki - 基于 Karpathy gist 的知识管理系统"""
    pass

@cli.command()
def init():
    """初始化 wiki 和 personal 目录结构"""
    base_path = Path.cwd()

    init_wiki_structure(base_path, 'wiki')
    init_wiki_structure(base_path, 'personal')

    # 创建 raw 目录
    (base_path / 'raw' / 'assets').mkdir(parents=True, exist_ok=True)

    click.echo('✓ Wiki 和 Personal 目录结构已初始化')

@cli.command()
@click.argument('target_or_file')
@click.argument('file', required=False)
def ingest(target_or_file, file):
    """导入文档到 wiki 或 personal

    用法：
      ingest <file>           → 导入到 wiki
      ingest personal <file>  → 导入到 personal
    """
    # 解析参数
    if file is None:
        # 单参数：默认 wiki
        target = 'wiki'
        source_path = target_or_file
    else:
        # 双参数：指定目标
        target = target_or_file
        source_path = file

    if target not in ['wiki', 'personal']:
        click.echo(f'错误: target 必须是 wiki 或 personal，收到: {target}', err=True)
        raise click.Abort()

    config = _load_config()
    llm = _create_llm(config)

    source_file = Path(source_path)
    if not source_file.exists():
        click.echo(f'错误: 文件不存在: {source_file}', err=True)
        raise click.Abort()

    wiki_dir = Path.cwd() / target
    index_file = wiki_dir / 'index.md'
    log_file = wiki_dir / 'log.md'

    result = ingest_document(source_file, wiki_dir, index_file, log_file, llm)

    click.echo(f'✓ 处理 {source_file.name}，创建 {len(result["pages"])} 个页面')

@cli.command()
@click.argument('question')
def query(question):
    """查询 wiki（自动检测 wiki/personal）"""
    config = _load_config()
    llm = _create_llm(config)
    base_path = Path.cwd()

    result = query_wiki_auto(question, base_path, llm)
    click.echo(f"\n{result['answer']}\n")
    if result['sources']:
        click.echo("来源:")
        for source in result['sources']:
            click.echo(f"  - {source}")

@cli.command()
@click.argument('keyword')
def search(keyword):
    """搜索 wiki 内容"""
    config = _load_config()
    wiki_dir = Path(config['paths']['wiki'])

    results = search_wiki(wiki_dir, keyword, max_results=config['search']['max_results'])
    if not results:
        click.echo('未找到结果')
        return

    click.echo(f'找到 {len(results)} 个结果:\n')
    for r in results:
        click.echo(f"{r['file']}:{r['line']}")
        click.echo(f"  {r['content']}\n")

@cli.command()
def lint():
    """检查 wiki 和 personal 健康状况"""
    base_path = Path.cwd()

    issues = lint_dual_wiki(base_path)
    if not issues:
        click.echo('✓ Wiki 和 Personal 健康状况良好')
        return

    click.echo(f'发现 {len(issues)} 个问题:\n')
    for issue in issues:
        click.echo(f'  {issue}')

def _load_config():
    """加载配置文件"""
    config_file = Path('config.yaml')
    if not config_file.exists():
        click.echo('错误: config.yaml 不存在', err=True)
        raise click.Abort()

    with open(config_file) as f:
        config = yaml.safe_load(f)

    if 'api_key' in config['llm']:
        api_key = config['llm']['api_key']
        if api_key.startswith('${') and api_key.endswith('}'):
            env_var = api_key[2:-1]
            # Try both ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN
            config['llm']['api_key'] = os.getenv(env_var) or os.getenv('ANTHROPIC_AUTH_TOKEN', '')

    return config

def _create_llm(config):
    """创建 LLM provider"""
    provider = config['llm']['provider']
    if provider == 'claude':
        return ClaudeProvider(
            api_key=config['llm']['api_key'],
            model=config['llm']['model']
        )
    elif provider == 'ollama':
        return OllamaProvider(model=config['llm']['model'])
    else:
        raise ValueError(f'Unknown provider: {provider}')

if __name__ == '__main__':
    cli()

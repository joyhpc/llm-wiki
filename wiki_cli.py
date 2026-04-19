#!/usr/bin/env python3
import click
import yaml
from pathlib import Path
from core.llm import ClaudeProvider, OllamaProvider
from core.ingest import ingest_document
from core.query import query_wiki
from core.search import search_wiki
from core.lint import lint_wiki
from utils.file_ops import ensure_dirs, write_file
import os

@click.group()
def cli():
    """LLM Wiki - 基于 Karpathy gist 的知识管理系统"""
    pass

@cli.command()
def init():
    """初始化 wiki 目录结构"""
    base_path = Path.cwd()
    ensure_dirs(base_path)

    if not (base_path / 'index.md').exists():
        write_file(base_path / 'index.md', '# Wiki Index\n\n')
    if not (base_path / 'log.md').exists():
        write_file(base_path / 'log.md', '# Wiki Log\n\n')
    if not (base_path / 'schema.md').exists():
        write_file(base_path / 'schema.md', '# Wiki Schema\n\n')

    click.echo('✓ Wiki 目录结构已初始化')

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def ingest(file):
    """导入文档到 wiki"""
    config = _load_config()
    llm = _create_llm(config)

    source_file = Path(file)
    wiki_dir = Path(config['paths']['wiki'])
    index_file = Path(config['paths']['index'])
    log_file = Path(config['paths']['log'])

    wiki_page = ingest_document(source_file, wiki_dir, index_file, log_file, llm)
    click.echo(f'✓ 已导入: {source_file.name} -> {wiki_page.name}')

@cli.command()
@click.argument('question')
def query(question):
    """查询 wiki"""
    config = _load_config()
    llm = _create_llm(config)
    wiki_dir = Path(config['paths']['wiki'])

    result = query_wiki(question, wiki_dir, llm)
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
    """检查 wiki 健康状况"""
    config = _load_config()
    wiki_dir = Path(config['paths']['wiki'])

    issues = lint_wiki(wiki_dir)
    if not issues:
        click.echo('✓ Wiki 健康状况良好')
        return

    click.echo(f'发现 {len(issues)} 个问题:\n')
    for issue in issues:
        click.echo(f'  - {issue}')

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
            config['llm']['api_key'] = os.getenv(env_var, '')

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

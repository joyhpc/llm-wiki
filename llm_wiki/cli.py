#!/usr/bin/env python3
import click
import yaml
from pathlib import Path
from llm_wiki.core.llm import ClaudeProvider, OllamaProvider
from llm_wiki.core.ingest import ingest_document
from llm_wiki.core.query import query_wiki_auto
from llm_wiki.core.search import search_wiki
from llm_wiki.core.lint import lint_dual_wiki
from llm_wiki.utils.init_wiki import init_wiki_structure
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

@cli.command()
@click.argument('target', type=click.Choice(['wiki', 'personal']))
@click.argument('category', type=click.Choice(['concepts', 'entities']))
@click.option('--threshold', default=0.8, help='相似度阈值 (0-1)')
@click.option('--auto-merge', is_flag=True, help='自动合并相似页面')
def merge(target, category, threshold, auto_merge):
    """查找并合并相似页面

    用法：
      merge personal concepts --threshold 0.8
      merge wiki entities --auto-merge
    """
    from llm_wiki.core.merge import find_similar_pages, merge_pages, update_references
    from llm_wiki.core.merge_optimizer import optimize_merge_order
    from llm_wiki.core.archive import archive_old_version

    base_path = Path.cwd()
    wiki_dir = base_path / target

    if not wiki_dir.exists():
        click.echo(f'错误: {target}/ 不存在', err=True)
        return

    config = _load_config()
    llm = _create_llm(config)

    click.echo(f'正在查找 {target}/{category}/ 中的相似页面...')
    similar_pairs = find_similar_pages(wiki_dir, category, llm, threshold)

    if not similar_pairs:
        click.echo('✓ 未发现相似页面')
        return

    click.echo(f'\n发现 {len(similar_pairs)} 对相似页面')

    # 优化合并顺序
    merge_tasks = optimize_merge_order(similar_pairs)
    click.echo(f'优化后：{len(merge_tasks)} 个合并任务\n')

    for primary, secondaries in merge_tasks[:10]:
        click.echo(f'  {primary} ← {", ".join(secondaries[:3])}{"..." if len(secondaries) > 3 else ""}')

    if not auto_merge:
        click.echo('\n使用 --auto-merge 标志自动合并这些页面')
        return

    # 自动合并
    click.echo('\n开始合并...')
    merged_count = 0

    for primary, secondaries in merge_tasks:
        click.echo(f'\n合并到 {primary}（{len(secondaries)} 个页面）...')

        primary_path = f'{category}/{primary}'
        primary_file = wiki_dir / primary_path

        # 检查主页面是否存在
        if not primary_file.exists():
            click.echo(f'  ⚠️ 跳过：主页面 {primary} 不存在')
            continue

        # 逐个合并次页面
        for secondary in secondaries:
            secondary_path = f'{category}/{secondary}'
            secondary_file = wiki_dir / secondary_path

            # 检查次页面是否存在
            if not secondary_file.exists():
                click.echo(f'  ⚠️ 跳过：{secondary} 已不存在')
                continue

            # 合并内容
            try:
                merged_content = merge_pages(wiki_dir, primary_path, secondary_path, llm)

                # 归档次页面
                archive_old_version(wiki_dir, secondary_path)

                # 写入主页面
                primary_file.write_text(merged_content, encoding='utf-8')

                # 更新所有引用
                update_references(wiki_dir, secondary, primary)

                # 删除次页面（如果还存在）
                if secondary_file.exists():
                    secondary_file.unlink()

                merged_count += 1
                click.echo(f'  ✓ 已合并 {secondary}')

            except Exception as e:
                click.echo(f'  ✗ 合并 {secondary} 失败: {e}')

    click.echo(f'\n✓ 完成！成功合并了 {merged_count} 个页面')

@cli.command()
@click.argument('target', type=click.Choice(['wiki', 'personal']))
@click.argument('page')
def references(target, page):
    """查看引用指定页面的所有页面

    用法：
      references personal gwcphy.md
      references wiki mipi-interface.md
    """
    from llm_wiki.core.cascade import get_referencing_pages, cascade_update_summary

    base_path = Path.cwd()
    wiki_dir = base_path / target

    if not wiki_dir.exists():
        click.echo(f'错误: {target}/ 不存在', err=True)
        return

    summary = cascade_update_summary(wiki_dir, page)

    if summary['total_references'] == 0:
        click.echo(f'✓ 没有页面引用 {page}')
        return

    click.echo(f'\n{page} 被 {summary["total_references"]} 个页面引用:\n')

    for category, pages in summary['by_category'].items():
        click.echo(f'\n{category.title()}:')
        for p in pages:
            click.echo(f'  - {p}')

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

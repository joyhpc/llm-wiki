import subprocess
from pathlib import Path
from typing import List, Dict

def search_wiki(wiki_dir: Path, query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """使用 ripgrep 搜索 wiki 内容"""
    try:
        result = subprocess.run(
            ['rg', '--json', '-i', query, str(wiki_dir)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return []

        matches = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            import json
            data = json.loads(line)
            if data.get('type') == 'match':
                matches.append({
                    'file': data['data']['path']['text'],
                    'line': data['data']['line_number'],
                    'content': data['data']['lines']['text'].strip()
                })
                if len(matches) >= max_results:
                    break

        return matches
    except FileNotFoundError:
        return _fallback_search(wiki_dir, query, max_results)

def _fallback_search(wiki_dir: Path, query: str, max_results: int) -> List[Dict[str, str]]:
    """简单的文本搜索回退"""
    matches = []
    for file_path in wiki_dir.glob('**/*.md'):
        content = file_path.read_text(encoding='utf-8')
        for i, line in enumerate(content.split('\n'), 1):
            if query.lower() in line.lower():
                matches.append({
                    'file': str(file_path),
                    'line': i,
                    'content': line.strip()
                })
                if len(matches) >= max_results:
                    return matches
    return matches

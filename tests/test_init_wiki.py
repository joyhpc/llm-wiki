import pytest
from pathlib import Path
from utils.init_wiki import init_wiki_structure

def test_init_wiki_structure(tmp_path):
    init_wiki_structure(tmp_path, 'wiki')

    assert (tmp_path / 'wiki' / 'index.md').exists()
    assert (tmp_path / 'wiki' / 'log.md').exists()
    assert (tmp_path / 'wiki' / 'sources').is_dir()
    assert (tmp_path / 'wiki' / 'concepts').is_dir()
    assert (tmp_path / 'wiki' / 'entities').is_dir()
    assert (tmp_path / 'wiki' / 'comparisons').is_dir()
    assert (tmp_path / 'wiki' / 'questions').is_dir()

def test_init_personal_structure(tmp_path):
    init_wiki_structure(tmp_path, 'personal')

    assert (tmp_path / 'personal' / 'index.md').exists()
    assert (tmp_path / 'personal' / 'log.md').exists()
    assert (tmp_path / 'personal' / 'reflections').is_dir()

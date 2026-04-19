import pytest
from core.router import detect_query_target

def test_detect_wiki_default():
    assert detect_query_target("What is Transformer?") == "wiki"
    assert detect_query_target("Explain attention mechanism") == "wiki"

def test_detect_personal_keywords():
    assert detect_query_target("我的项目架构是什么？") == "personal"
    assert detect_query_target("我之前怎么处理的？") == "personal"
    assert detect_query_target("查 personal：反思记录") == "personal"
    assert detect_query_target("What did I do in project X?") == "personal"

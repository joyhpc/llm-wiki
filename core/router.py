def detect_query_target(question: str) -> str:
    """检测查询目标：wiki 或 personal"""
    question_lower = question.lower()

    # personal 触发词
    personal_triggers = [
        'personal', '我的', '我之前', '我曾经',
        'my ', 'i did', 'i have', 'i worked', 'did i'
    ]

    for trigger in personal_triggers:
        if trigger in question_lower:
            return 'personal'

    return 'wiki'  # 默认

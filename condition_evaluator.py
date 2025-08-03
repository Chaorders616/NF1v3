# condition_evaluator.py

def select_best_branch(options, clip_text):
    """
    从多个分支中选择最可能满足条件的路径。
    当前使用关键词粗匹配作为启发式策略，可升级为语义嵌入或GPT评估。
    """
    clip_text = clip_text.lower()
    for option in options:
        condition = option.get("condition", "").lower()
        if condition and condition in clip_text:
            return option["target"]
    return options[0]["target"]  # fallback 回退策略

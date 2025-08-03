
def compile_style(style_dict):
    """
    根据传入的风格字典，从本地样式库中加载具体风格参数。
    """
    tone = style_dict.get("tone", "neutral")
    sentence_form = style_dict.get("sentence_form", "balanced")
    syntax_pattern = style_dict.get("syntax_pattern", "X. Y. Z.")

    return {
        "tone": tone,
        "sentence_form": sentence_form,
        "syntax_pattern": syntax_pattern
    }

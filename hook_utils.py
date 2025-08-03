# hook_utils.py - 包含 inject_recall_hint 和 evaluate_hook_usage

from model_executor import run_gpt


def inject_recall_hint(prompt: str, hook: dict) -> str:
    """
    将 Hook 信息结构性注入到 prompt 中。
    """
    hook_text = hook.get("hook_text", "")
    function = hook.get("narrative_function", "")
    recall_style = hook.get("structure_constraints", {}).get("recommended_recall_style", "")

    hint = f"\n---\nPlease continue the story, and recall the following narrative hook:\n"
    hint += f"Hook: \"{hook_text}\"\n"
    hint += f"Function: {function}\n"
    if recall_style:
        hint += f"Recommended recall style: {recall_style}\n"

    return prompt.strip() + hint


def evaluate_hook_usage(text: str, hook: dict) -> dict:
    """
    使用 GPT 判定文本是否有效回应钩子。
    """
    hook_text = hook.get("hook_text", "")
    prompt = f"""
你是一个叙事结构分析师，请判断以下文本是否回应了指定的钩子：

钩子内容：\n"{hook_text}"

待评估文本：\n{text}

回应的定义是：文本内容对钩子所表达的情绪、问题、未解事件、结构性暗示等有明确的推进、回应、反转或补充。

请按以下格式回答：
- recall_score: 0.0 到 1.0（数值）
- reason: 简要说明是否以及如何回应

JSON输出：
"""
    response = run_gpt(prompt)
    try:
        return eval(response.strip())
    except Exception as e:
        return {
            "recall_score": 0.0,
            "reason": f"解析失败: {str(e)}",
            "raw_output": response
        }

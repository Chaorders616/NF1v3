# narrative_critic.py

from model_executor import run_gpt  # 复用已有 GPT 调用工具

def critique_clip_structure(clip_text: str, context: str = "") -> dict:
    """
    调用 GPT 评估 clip 的结构合理性、节奏与动机逻辑，并生成评分与建议。
    返回结构:
    {
        "score": 0-10,
        "critique": "结构与逻辑分析",
        "rewrite_prompt": "建议提供给 AI 的重写提示语"
    }
    """
    prompt = f"""
你是一个叙事结构分析专家，请评估以下剧情片段（clip）是否具有良好的结构完整性、角色动机表达与情绪张力。

你需要返回 JSON 格式，字段如下：
- score: 0-10 分，表示结构完整性
- critique: 指出该片段的结构优劣、节奏问题或角色行为逻辑是否合理
- rewrite_prompt: 如果要让 AI 重写这段剧情，你建议的提示语是什么？

=== Clip 内容 ===
{clip_text}

=== 剧情上下文（可选） ===
{context if context else "（无）"}
"""

    response = run_gpt(prompt)
    try:
        return eval(response.strip())  # 简易解析，可换成 json.loads() 视返回格式而定
    except:
        return {"score": 0, "critique": "评分解析失败", "rewrite_prompt": ""}

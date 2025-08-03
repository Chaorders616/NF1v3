def inject_impact(prompt, impact_dict):
    """
    注入冲击控制提示（如 pivot 句、情绪跳跃说明等）。
    """
    impact_prompt = prompt
    if impact_dict.get("pivot_required"):
        impact_prompt += f"\nInclude a pivotal line like: '{impact_dict.get('pivot_hint')}'."
    if impact_dict.get("emotion_jump"):
        impact_prompt += f"\nThe emotional shift should be: {impact_dict['emotion_jump']}."
    return impact_prompt

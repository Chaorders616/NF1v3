# prompt_assembler.py（支持 resolve_hook_id 注入）

def assemble_prompt(clip_text: str, style_cfg: dict, impact_cfg: dict, hook_hint: str = None, resolve_id: str = None) -> str:
    """
    组装用于 GPT 的 prompt，支持风格控制、冲击控制、hook 回忆提示、明确回忆目标（resolve_id）
    """
    style_part = f"Style: tone={style_cfg.get('tone')}, form={style_cfg.get('sentence_form')}, syntax={style_cfg.get('syntax_pattern')}"
    impact_part = f"Impact: pivot_required={impact_cfg.get('pivot_required')}, emotion_jump={impact_cfg.get('emotion_jump')}"

    hook_part = f"HookHint: Try to recall or resolve → {hook_hint}" if hook_hint else ""
    resolve_part = f"ResolveHookID: {resolve_id}" if resolve_id else ""

    return f"""
        Generate a dramatic scene based on the following sketch:

        Scene Sketch:
        {clip_text}

        {style_part}
        {impact_part}
        {hook_part}
        {resolve_part}
            """.strip()

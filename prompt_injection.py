# prompt_injection.py - 为 ClipForge 注入结构任务提示与回响提示

def inject_recall_hint(roles: dict, phase: dict, hook: dict = None) -> str:
    """根据结构意图 + 回忆钩子，构建最终提示语"""
    setting = phase.get("setting", "a location")
    intent = phase.get("intent", "initiate_conflict")
    phase_type = phase.get("type", "Scene")

    # 角色介绍文本
    role_texts = [f"{k}: {v.brief}" for k, v in roles.items() if hasattr(v, 'brief')]
    role_hint = "\n".join(role_texts)

    # 回忆钩子文本
    recall_text = ""
    if hook:
        recall_text = f"\n---\nPlease continue the story, and recall the following narrative hook:\nHook: \"{hook['hook_text']}\"\nFunction: {hook['narrative_function']}\nRecommended recall style: {hook.get('structure_constraints', {}).get('recommended_recall_style', 'direct')}"

    # 总体任务提示
    prompt = f"""
Scene Phase: {phase_type}
Intent: {intent}
Setting: {setting}

Characters:
{role_hint}

Start writing a dramatic scene between these characters that fulfills the narrative intent.
{recall_text}
    """
    return prompt.strip()

# clip_forge_v2.py - Hook驱动的Clip生成引擎（闭环结构）

from model_executor import run_gpt
from hook_classifier import classify_hook_text
from hook_registry import HookRegistry
from hook_utils import inject_recall_hint, evaluate_hook_usage
from hook_recall_engine_v2 import HookRecallEngine


def generate_clip_from_phase(phase: dict, roles: dict, registry: HookRegistry) -> dict:
    """
    为单个phase生成带Hook的Clip，包含结构识别、prompt注入、结构评估闭环。
    """
    role_names = list(roles.keys())
    a_name, b_name = role_names[0], role_names[1]
    setting = phase.get("setting", "a quiet room")
    intent = phase.get("intent", "confrontation")
    duration = phase.get("duration", 1)
    phase_type = phase.get("type", "Unknown")

    # 构造基础Prompt
    base_prompt = f"Scene type: {phase_type}\nSetting: {setting}\nDuration: {duration} min\n"
    base_prompt += f"Characters: {a_name} and {b_name}\n"
    base_prompt += f"Intent: {intent}\n"

    # Recall最适合的结构钩子，注入到 prompt
    recaller = HookRecallEngine(registry)
    candidates = recaller.get_recall_candidates(current_function=intent, current_phase=phase_type)
    hook_used = None
    if candidates:
        hook_used = candidates[0]
        base_prompt = inject_recall_hint(base_prompt, hook_used)

    # 调用GPT生成内容
    response = run_gpt(base_prompt)

    # 提取新生成内容中的结构性钩子
    new_hook_result = classify_hook_text(response)
    if new_hook_result.get("is_hook"):
        registry.register_hook(
            clip_id=f"{phase_type}_{a_name}_{b_name}",
            hook_text=new_hook_result["hook_text"] if "hook_text" in new_hook_result else response.split("\n")[0],
            narrative_function=new_hook_result["narrative_function"],
            function_hierarchy=new_hook_result["function_hierarchy"],
            intent_signals=new_hook_result["intent_signals"],
            structure_constraints=new_hook_result["structure_constraints"]
        )

    # 回应钩子 → 评估是否闭环
    if hook_used:
        score = evaluate_hook_usage(response, hook_used)
        if score.get("recall_score", 0.0) > 0.6:
            registry.mark_hook_as_used(hook_used["hook_id"])

    # 返回生成片段结构
    return {
        "phase": phase,
        "clip_text": response,
        "recall_used": hook_used["hook_id"] if hook_used else None,
        "new_hook_detected": new_hook_result if new_hook_result.get("is_hook") else None
    }

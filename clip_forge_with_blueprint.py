# clip_forge_with_blueprint.py - 集成 Blueprint 的结构驱动型 ClipForge

from hook_registry import HookRegistry
from hook_recall_engine_v2 import HookRecallEngine
from hook_classifier import classify_hook_text
from hook_evaluator import evaluate_hook_usage
from story_blueprint_system import StoryBlueprint
from prompt_injection import inject_recall_hint
from gpt_interface import run_gpt


def generate_clip_with_blueprint(phase, roles, registry: HookRegistry, blueprint: StoryBlueprint):
    # 准备结构提示
    phase_type = phase.get("type")
    intent = phase.get("intent")
    setting = phase.get("setting")

    recaller = HookRecallEngine(registry)
    candidates = recaller.get_recall_candidates(current_function=intent, current_phase=phase_type)
    selected_hook = candidates[0] if candidates else None

    prompt = inject_recall_hint(roles, phase, selected_hook)
    output_text = run_gpt(prompt)

    # Step 1️⃣ 结构钩子分类（新钩子）
    new_hook = classify_hook_text(output_text, phase, clip_id=f"{phase_type}_CLIP")
    if new_hook:
        registry.register_hook(new_hook)
        # 检查是否满足蓝图结构要求
        blueprint.resolve_phase_by_hook(new_hook["hook_id"], new_hook["narrative_function"])

    # Step 2️⃣ 结构钩子回响检测（回应旧钩子）
    if selected_hook:
        recall_score = evaluate_hook_usage(output_text, selected_hook)
        if recall_score.get("recall_score", 0) > 0.5:
            registry.mark_used(selected_hook["hook_id"])
            recalled_hook_id = selected_hook["hook_id"]
        else:
            recalled_hook_id = None
    else:
        recalled_hook_id = None

    return {
        "phase": phase,
        "clip_text": output_text,
        "recall_used": recalled_hook_id,
        "new_hook_detected": new_hook
    }

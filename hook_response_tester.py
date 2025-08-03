# hook_response_tester.py - 测试结构闭环：inject → run → evaluate → mark used

from hook_registry import HookRegistry
from hook_recall_engine_v2 import HookRecallEngine
from hook_utils import inject_recall_hint, evaluate_hook_usage
from model_executor import run_gpt

# 初始化 Hook 系统
registry = HookRegistry()
recaller = HookRecallEngine(registry)

# 手动注册一个 Hook（模拟 hook_classifier 输出）
hook_id = registry.register_hook(
    clip_id="demo_clip",
    hook_text="You said you'd never leave me. But you're gone.",
    narrative_function="escalate_tension",
    function_hierarchy=["drive_conflict", "escalate_tension"],
    intent_signals={
        "emotion": {"value": "sadness", "weight": 0.8},
        "relationship_change": {"value": "betrayal", "weight": 0.9},
        "truth_status": {"value": "deception", "weight": 0.7},
        "stakes": {"value": "loss of trust", "weight": 0.8}
    },
    structure_constraints={
        "expected_resolution_phase": "Climax",
        "recommended_recall_style": "direct_confrontation",
        "reversal_conditions": {
            "probability": 0.6,
            "trigger": ["apology not accepted", "revelation of the truth"],
            "effect": "ultimate confrontation and resolution of the conflict"
        },
        "delay_priority": 0.3
    }
)

# 获取候选 Hook
hook = recaller.get_recall_candidates(current_function="escalate_tension", current_phase="Climax")[0]

# 构造 Prompt
base_prompt = "A now confronts B in the aftermath of betrayal."
prompt = inject_recall_hint(base_prompt, hook)

print("\n===== 最终 Prompt =====\n")
print(prompt)

# 模拟生成文本（或真实调用 GPT）
response_text = run_gpt(prompt)
print("\n===== GPT 生成回应文本 =====\n")
print(response_text)

# 评估结构回应效果
score_info = evaluate_hook_usage(response_text, hook)
print("\n===== 钩子回应评分 =====\n")
print(score_info)

# 若得分高，标记为 used
if score_info.get("recall_score", 0.0) > 0.6:
    registry.mark_hook_as_used(hook["hook_id"])
    print(f"\n[✅] Hook {hook['hook_id']} 已标记为已使用")
else:
    print(f"\n[⚠️] Hook {hook['hook_id']} 尚未被充分回应")

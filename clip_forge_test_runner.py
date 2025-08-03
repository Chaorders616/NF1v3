# clip_forge_test_runner.py - 批量测试Clip生成闭环

from clip_forge_v2 import generate_clip_from_phase
from hook_registry import HookRegistry

# 示例角色表
roles = {
    "A": {"name": "A", "traits": ["emotional", "driven"]},
    "B": {"name": "B", "traits": ["secretive", "logical"]},
}

# 示例 Phase Blueprint
PHASE_GRAPH = [
    {"type": "Introduction", "duration": 1, "intent": "introduce_setting", "setting": "Office"},
    {"type": "Inciting Incident", "duration": 1, "intent": "initiate_conflict", "setting": "Corridor"},
    {"type": "Escalation", "duration": 2, "intent": "escalate_tension", "setting": "Warehouse"},
    {"type": "Climax", "duration": 2, "intent": "raise_emotional_stake", "setting": "Rooftop"},
    {"type": "Resolution", "duration": 1, "intent": "resolve_dispute", "setting": "Street"},
]

# 初始化 HookRegistry
registry = HookRegistry()

print("===== ClipForge Hook化测试开始 =====\n")

# 逐段生成 Clip
for i, phase in enumerate(PHASE_GRAPH):
    print(f"\n--- 第{i+1}段 Phase: {phase['type']} ---")
    result = generate_clip_from_phase(phase, roles, registry)
    print("\n🎬 生成内容：\n", result["clip_text"][:500], "...")
    print("\n📌 回应钩子：", result["recall_used"])
    if result["new_hook_detected"]:
        print("🧠 新钩子类型：", result["new_hook_detected"].get("narrative_function"))

# 总结 Hook 状态
print("\n===== Hook 使用情况 =====")
all_hooks = registry.hooks
for h in all_hooks:
    status = "✅ 已回应" if h["used"] else "❗待回应"
    print(f"- {h['hook_id']} | {h['narrative_function']} | {status}")

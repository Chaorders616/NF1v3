# hook_test_runner.py - 一体化测试链：分类 → 注册 → 回忆

from hook_classifier import classify_hook_text
from hook_registry import HookRegistry
from hook_recall_engine_v2 import HookRecallEngine

# 初始化系统组件
registry = HookRegistry()
recaller = HookRecallEngine(registry)

def run_test_on_sentence(text: str, context: str = "", clip_id: str = "demo_clip"):
    print("\n===== 原始句子 =====")
    print(text)

    result = classify_hook_text(text, context)
    if not result.get("is_hook"):
        print("\n[❌] 此句未被判定为结构性 Hook")
        return

    print("\n[✅] Hook 结构识别结果：")
    print("Function:", result["narrative_function"])
    print("Hierarchy:", result["function_hierarchy"])
    print("Signals:", result["intent_signals"])
    print("Constraints:", result["structure_constraints"])

    # 注册
    hook_id = registry.register_hook(
        clip_id=clip_id,
        hook_text=text,
        narrative_function=result["narrative_function"],
        function_hierarchy=result["function_hierarchy"],
        intent_signals=result["intent_signals"],
        structure_constraints=result["structure_constraints"]
    )
    print(f"\n[📌] Hook 已注册，ID: {hook_id}")

    # 回忆
    print("\n===== 回忆引擎筛选钩子候选 =====")
    candidates = recaller.get_recall_candidates(current_function="raise_emotional_stake", current_phase="Climax")
    for i, h in enumerate(candidates):
        print(f"#{i+1} | {h['hook_id']} ({h['narrative_function']}) → {h['hook_text']}")

# 示例句子
test_line = "You said you'd never leave me. But you're gone."
run_test_on_sentence(test_line)

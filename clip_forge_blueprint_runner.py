# clip_forge_blueprint_runner.py - Blueprint驱动Clip生成全流程执行器（+自动修复器模块 + 弹性结构升级 + 张力检测模块 + 多角色结构支持 + 分支结构支持 + 条件评估器接入 + 分支路径可视化增强 + 📍分支路径追踪器ClipPathTracker初始化 + 🔄 角色视角控制系统初步接入）

from blueprint_generator import build_blueprint
from hook_registry import HookRegistry
from clip_forge_with_blueprint import generate_clip_with_blueprint
from hook_coverage_reporter import analyze_function_coverage
from story_blueprint_system import StoryBlueprint
from prompt_injection import inject_recall_hint
from gpt_interface import run_gpt

# ✅ 新增导出和评分模块
from collections import Counter
import random

# 📍 分支路径追踪器：记录经历过的clip路径结构
clip_path_trace = []

# 📌 角色回应记录表（role_id → responded_hooks 列表）
role_response_log = {}

def log_role_response(role_id, hook_id):
    role_response_log.setdefault(role_id, []).append(hook_id)

def choose_responder(hook_id):
    from hook_registry import global_registry  # 假设 registry 是模块级变量
    hook = global_registry.get_hook_by_id(hook_id)
    if not hook:
        return "A"
    signals = hook.get("intent_signals", {})
    emo = signals.get("emotion", {}).get("value", "").lower()
    rel = signals.get("relationship_change", {}).get("value", "").lower()
    if emo in ["guilt", "remorse"] or rel == "abandonment":
        return "B"
    elif emo in ["betrayal", "grief"] or rel == "trust_broken":
        return "A"
    return "A"

def score_blueprint_completion(blueprint: StoryBlueprint):
    total = len([p for p in blueprint.phases if p.constraint_level != "free"])
    completed = sum(1 for p in blueprint.phases if p.hook_resolved or p.constraint_level == "free")
    unresolved = total - completed
    percent = round(completed / total * 100, 1) if total else 100
    return {
        "total_phases": total,
        "completed_phases": completed,
        "unresolved_phases": unresolved,
        "completion_percent": percent
    }

def score_tension_curve(blueprint: StoryBlueprint):
    function_tension_map = {
        "build_emotion": 1.0,
        "introduce_context": 1.0,
        "initiate_conflict": 3.0,
        "escalate_conflict": 4.0,
        "resolve_conflict": 5.0,
        "emotional_resolution": 2.0,
        "reveal_secret": 2.5,
        "close_loop": 2.0,
    }
    ideal_curve = [1.0, 2.5, 4.0, 5.0, 2.0]
    tension_scores = []
    for i, phase in enumerate(blueprint.phases):
        fn = phase.expected_function
        score = function_tension_map.get(fn, 2.0)
        tension_scores.append(score)
        print(f"{phase.phase_id} | {phase.phase_type:20} | {fn:20} → 张力: {score}")
    min_len = min(len(tension_scores), len(ideal_curve))
    deviation = sum(abs(tension_scores[i] - ideal_curve[i]) for i in range(min_len)) / min_len
    print(f"\n偏离度: {round(deviation, 2)} → 🎯 张力健康度: {"优秀" if deviation < 0.8 else "良好" if deviation < 1.5 else "偏弱"}")

def export_blueprint_graphviz(blueprint: StoryBlueprint, filepath: str = "blueprint_graph.dot"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("digraph Blueprint {\n")
        f.write("  rankdir=LR;\n  node [shape=box, style=rounded];\n")
        for phase in blueprint.phases:
            node_id = phase.phase_id
            label = f"{phase.phase_type}\n({phase.expected_function})\n[{phase.constraint_level}]"
            style = "filled" if phase.hook_resolved else "dashed"
            color = {"strict": "lightblue", "flexible": "lightgreen", "free": "yellow"}.get(phase.constraint_level, "gray")
            if phase.hook_data and phase.hook_data.get("hook_type") == "soft":
                style += ",dotted"
            f.write(f'  {node_id} [label="{label}", style={style}, fillcolor={color}];\n')
        for phase in blueprint.phases:
            if hasattr(phase, "next_phase_options") and phase.next_phase_options:
                for option in phase.next_phase_options:
                    f.write(f'  {phase.phase_id} -> {option["target"]} [label="{option["condition"]}"];\n')
            else:
                i = blueprint.phases.index(phase)
                if i < len(blueprint.phases) - 1:
                    f.write(f"  {phase.phase_id} -> {blueprint.phases[i+1].phase_id};\n")
        f.write("}\n")
    print(f"\n📤 Blueprint结构图已导出为: {filepath}")

def gpt_review_blueprint(blueprint: StoryBlueprint) -> str:
    blueprint_summary = "\n".join([
        f"{p.phase_id} | {p.phase_type} | {p.expected_function} → {p.resolved_by_hook_id or '[未完成]'}"
        for p in blueprint.phases
    ])
    prompt = f"""
You are a narrative design reviewer. Analyze the following story blueprint's structural completeness and consistency.
Blueprint Summary:
{blueprint_summary}

Please comment on:
- Whether the structure covers a full arc
- Which phases lack proper resolution
- Suggestions for improving the narrative balance
Respond in markdown.
"""
    print("\n===== GPT结构评估报告（模拟） =====")
    response = run_gpt(prompt)
    print(response)
    return response

def autofix_unresolved_phases(blueprint: StoryBlueprint, roles, registry: HookRegistry):
    print("\n===== ⛑ 自动修复器开始执行 =====")
    fixed = 0
    for phase in blueprint.phases:
        if not phase.hook_resolved and phase.constraint_level != "free":
            phase_data = phase.as_dict()
            prompt = inject_recall_hint(roles, phase_data, hook=None)
            result = generate_clip_with_blueprint(phase_data, roles, registry, blueprint)
            if result["new_hook_detected"]:
                print(f"✅ 自动修复阶段 {phase.phase_id} ({phase.phase_type}) 成功，生成hook: {result['new_hook_detected']['hook_text'][:60]}...")
                fixed += 1
            else:
                print(f"⚠️ 自动修复阶段 {phase.phase_id} 失败，未生成有效hook")
    print(f"\n✅ 自动修复完成，共修复 {fixed} 个阶段\n")

def get_sample_roles():
    class Role:
        def __init__(self, brief):
            self.brief = brief
    return {
        "A": Role("a determined seeker with a painful past"),
        "B": Role("a mentor figure hiding a secret")
    }

if __name__ == "__main__":
    print("===== Blueprint ClipForge 执行测试开始 =====\n")

    roles = get_sample_roles()
    blueprint: StoryBlueprint = build_blueprint("HeroJourney", title="The Shattered Path", theme="Redemption")
    registry = HookRegistry()

    results = []
    current_phase_id = blueprint.phases[0].phase_id
    visited_phases = set()

    while current_phase_id:
        phase = blueprint.get_phase_by_id(current_phase_id)
        if not phase or current_phase_id in visited_phases:
            break

        visited_phases.add(current_phase_id)
        print(f"\n--- 阶段 {phase.phase_id}: {phase.phase_type} ({phase.expected_function}) ---")

        phase_data = phase.as_dict()
        intent = phase_data.get("expected_function")

        prompt = inject_recall_hint(roles, phase_data, hook=None)
        generated_text = run_gpt(prompt)

        result = generate_clip_with_blueprint(phase_data, roles, registry, blueprint, looseness=0.3)

        print("\n🎬 生成内容：\n", result["clip_text"][:500])
        if result["recall_used"]:
            print("\n📌 回应钩子：", result["recall_used"])
            log_role_response("A", result["recall_used"])
        if result["new_hook_detected"]:
            print("🧠 新钩子类型：", result["new_hook_detected"]["narrative_function"])
        results.append(result)

        clip_path_trace.append(current_phase_id)

        # 条件分支判断（目前使用简化策略）
        if hasattr(phase, "next_phase_options") and phase.next_phase_options:
            from condition_evaluator import select_best_branch
            current_phase_id = select_best_branch(phase.next_phase_options, result["clip_text"])
        else:
            idx = blueprint.phases.index(phase)
            current_phase_id = blueprint.phases[idx + 1].phase_id if idx + 1 < len(blueprint.phases) else None

    print("\n===== Hook 使用情况结构分析 =====")
    analyze_function_coverage(registry)

    print("\n===== Blueprint 结构响应情况 =====")
    for p in blueprint.phases:
        print(f"{p.phase_id} | {p.phase_type} | {p.expected_function} → {p.resolved_by_hook_id or '❗未完成'}")

    autofix_unresolved_phases(blueprint, roles, registry)

    print("\n===== Blueprint 完成度评分 =====")
    score = score_blueprint_completion(blueprint)
    print(f"结构阶段总数: {score['total_phases']}\n已完成阶段: {score['completed_phases']}\n未完成阶段: {score['unresolved_phases']}\n结构完成度: {score['completion_percent']}%")

    print("\n===== 张力曲线分析 =====")
    score_tension_curve(blueprint)

    export_blueprint_graphviz(blueprint)
    gpt_review_blueprint(blueprint)

    print("\n===== 分支路径追踪结果 =====")
    print(" → ".join(clip_path_trace))
    print("\n===== 多角色回应记录 =====")
    for role, hooks in role_response_log.items():
        print(f"角色 {role} 回应了 {len(hooks)} 个钩子: {hooks}")

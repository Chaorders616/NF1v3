# hook_coverage_reporter.py - 分析结构功能覆盖情况

from hook_registry import HookRegistry
from hook_schema import narrative_function_hierarchy
from collections import defaultdict


def flatten_all_functions():
    """展开所有 narrative_function 到一个扁平列表"""
    flat = []
    for group, funcs in narrative_function_hierarchy.items():
        for f in funcs:
            flat.append((group, f))
    return flat


def analyze_function_coverage(registry: HookRegistry):
    hooks = registry.hooks
    found = defaultdict(list)
    used = set()

    for h in hooks:
        func = h.get("narrative_function")
        group = None
        for g, fs in narrative_function_hierarchy.items():
            if func in fs:
                group = g
                break
        if group:
            found[group].append((func, h["hook_id"], h["used"]))
        if h.get("used"):
            used.add(func)

    flat = flatten_all_functions()

    print("\n===== Narrative Function Coverage Report =====\n")
    for group, func in flat:
        status = "✅ USED" if func in used else ("📌 EXISTING" if any(f == func for f, *_ in found.get(group, [])) else "❗ MISSING")
        print(f"[{status}] {group:20} → {func}")

    print("\n===== Active Hook Status Summary =====")
    for group, hooks_in_group in found.items():
        print(f"\n🔹 {group.upper()} ({len(hooks_in_group)} hooks):")
        for func, hook_id, used_flag in hooks_in_group:
            flag = "✅" if used_flag else "🕗"
            print(f"  {flag} {func:25} ← {hook_id}")

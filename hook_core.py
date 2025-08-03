# hook_core.py

class HookRegistry:
    def __init__(self):
        self.hooks = []  # 存储所有注册钩子

    def register_hook(self, clip_id, hook_text, hook_type="general", strength=1.0):
        hook_id = f"{clip_id}_H{len(self.hooks)}"
        self.hooks.append({
            "hook_id": hook_id,
            "clip_id": clip_id,
            "hook_text": hook_text,
            "hook_type": hook_type,
            "strength": strength,
            "used": False
        })
        return hook_id

    def get_active_hooks(self):
        return [h for h in self.hooks if not h["used"]]

    def mark_hook_as_used(self, hook_id):
        for h in self.hooks:
            if h["hook_id"] == hook_id:
                h["used"] = True
                return True
        return False


class HookRecallEngine:
    def __init__(self, hook_registry: HookRegistry):
        self.hook_registry = hook_registry

    def get_recall_candidates(self, current_intent=None):
        active_hooks = self.hook_registry.get_active_hooks()
        # TODO: 按照 intent/strength 排序或筛选
        return active_hooks

    def inject_recall_hint(self, prompt, hook):
        if not hook:
            return prompt
        return prompt + f"\n(请尝试回应以下情节: \"{hook['hook_text']}\")"


class HookEvaluator:
    def __init__(self, hook_registry: HookRegistry):
        self.hook_registry = hook_registry

    def evaluate_hook_usage(self, text, hook):
        # 简单启发式：是否提及关键词（可以改为GPT判定）
        score = 1.0 if hook["hook_text"][:10].lower() in text.lower() else 0.0
        return {
            "hook_id": hook["hook_id"],
            "recall_score": score,
            "hook_summary": hook["hook_text"][:50] + "...",
            "suggestion": (
                "Hook recalled successfully." if score > 0.5 else
                f"Weak recall of [{hook['hook_type']}] hook. Consider reinforcing."
            )
        }

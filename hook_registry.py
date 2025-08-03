# hook_registry.py (v2) - 支持完整结构化 hook 注册

from typing import List, Dict, Optional

class HookRegistry:
    def __init__(self):
        self.hooks: List[Dict] = []

    def register_hook(self,
                      clip_id: str,
                      hook_text: str,
                      narrative_function: str,
                      function_hierarchy: List[str],
                      intent_signals: Dict[str, Dict[str, float]],
                      structure_constraints: Dict,
                      hook_type: str = "textual",
                      score: float = 1.0
                      ) -> str:
        hook_id = f"{clip_id}_H{len(self.hooks)}"
        hook = {
            "hook_id": hook_id,
            "clip_id": clip_id,
            "hook_type": hook_type,
            "hook_text": hook_text,
            "narrative_function": narrative_function,
            "function_hierarchy": function_hierarchy,
            "intent_signals": intent_signals,
            "structure_constraints": structure_constraints,
            "audience_impact": {},  # 可后续填充
            "used": False,
            "score": score,
            "derived_hooks": []
        }
        self.hooks.append(hook)
        return hook_id

    def get_active_hooks(self) -> List[Dict]:
        return [h for h in self.hooks if not h["used"]]

    def mark_hook_as_used(self, hook_id: str) -> bool:
        for h in self.hooks:
            if h["hook_id"] == hook_id:
                h["used"] = True
                return True
        return False

    def get_hook_by_id(self, hook_id: str) -> Optional[Dict]:
        return next((h for h in self.hooks if h["hook_id"] == hook_id), None)

    def get_hooks_by_function(self, func: str) -> List[Dict]:
        return [h for h in self.hooks if h["narrative_function"] == func and not h["used"]]

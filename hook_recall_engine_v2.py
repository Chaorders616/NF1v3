# hook_recall_engine_v2.py - 支持结构性钩子排序与调度

from typing import List, Optional, Dict
from hook_registry import HookRegistry

class HookRecallEngine:
    def __init__(self, registry: HookRegistry):
        self.registry = registry

    def get_recall_candidates(self,
                               current_function: Optional[str] = None,
                               current_phase: Optional[str] = None,
                               top_k: int = 3) -> List[Dict]:
        """
        返回当前最优先的未使用结构钩子，考虑结构任务匹配与延迟优先级
        """
        active_hooks = self.registry.get_active_hooks()
        scored = []

        for hook in active_hooks:
            constraints = hook.get("structure_constraints", {})
            delay_priority = constraints.get("delay_priority", 0.5)

            urgency = self._estimate_function_urgency(hook["narrative_function"])
            signal_strength = self._estimate_signal_strength(hook["intent_signals"])
            narrative_position = 0.5  # TODO: 待加入真实位置推断

            score = (0.4 * urgency) + (0.3 * signal_strength) + (0.3 * (1 - delay_priority))

            # 结构阶段兼容性加分
            if current_phase and constraints.get("expected_resolution_phase") == current_phase:
                score += 0.1

            # 功能匹配加分
            if current_function and hook["narrative_function"] == current_function:
                score += 0.1

            scored.append((hook, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [h for h, s in scored[:top_k]]

    def _estimate_function_urgency(self, function: str) -> float:
        urgency_map = {
            "initiate_conflict": 0.9,
            "raise_emotional_stake": 0.8,
            "resolve_dispute": 0.6,
            "introduce_setting": 0.3,
            "reveal_theme": 0.4
        }
        return urgency_map.get(function, 0.5)

    def _estimate_signal_strength(self, signals: Dict[str, Dict]) -> float:
        total = 0.0
        for field, conf in signals.items():
            weight = conf.get("weight", 0.3)
            total += weight
        return min(total, 1.0)

# story_blueprint_system.py - 叙事蓝图系统结构器

from typing import List, Dict
from hook_schema import narrative_function_hierarchy


class BlueprintPhase:
    def __init__(self, phase_id: str, phase_type: str, expected_function: str, constraints: Dict = None):
        self.phase_id = phase_id  # 如 'P1', 'P2', etc.
        self.phase_type = phase_type  # 如 'Introduction', 'Inciting', etc.
        self.expected_function = expected_function  # narrative_function
        self.constraints = constraints or {}  # 可包含 setting, required_roles, etc.
        self.hook_resolved = False
        self.resolved_by_hook_id = None

    def as_dict(self):
        return {
            "phase_id": self.phase_id,
            "phase_type": self.phase_type,
            "expected_function": self.expected_function,
            "constraints": self.constraints,
            "hook_resolved": self.hook_resolved,
            "resolved_by_hook_id": self.resolved_by_hook_id
        }


class StoryBlueprint:
    def __init__(self, title: str, theme: str, structure_type: str = "FiveAct"):
        self.title = title
        self.theme = theme
        self.structure_type = structure_type  # 可扩展为 'HeroJourney', 'Tragedy' 等
        self.phases: List[BlueprintPhase] = []

    def add_phase(self, phase_id, phase_type, expected_function, constraints=None):
        self.phases.append(BlueprintPhase(phase_id, phase_type, expected_function, constraints))

    def as_dict(self):
        return {
            "title": self.title,
            "theme": self.theme,
            "structure_type": self.structure_type,
            "phases": [p.as_dict() for p in self.phases]
        }

    def unresolved_functions(self):
        return [p.expected_function for p in self.phases if not p.hook_resolved]

    def resolve_phase_by_hook(self, hook_id: str, function: str):
        for p in self.phases:
            if p.expected_function == function and not p.hook_resolved:
                p.hook_resolved = True
                p.resolved_by_hook_id = hook_id
                return True
        return False

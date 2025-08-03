# five_act_blueprint_builder.py - 五幕式结构蓝图自动生成器

from story_blueprint_system import StoryBlueprint


def build_five_act_blueprint(title: str, theme: str = "Transformation") -> StoryBlueprint:
    blueprint = StoryBlueprint(title=title, theme=theme, structure_type="FiveAct")

    # 五幕结构默认配置
    blueprint.add_phase("P1", "Introduction", "build_trust", {"setting": "Office"})
    blueprint.add_phase("P2", "Inciting Incident", "initiate_conflict", {"required_roles": ["A", "B"]})
    blueprint.add_phase("P3", "Escalation", "reveal_secret", {"emotional_shift": "betrayal"})
    blueprint.add_phase("P4", "Climax", "raise_stakes", {"pressure": "deadline"})
    blueprint.add_phase("P5", "Resolution", "resolve_dispute", {"goal": "emotional_reckoning"})

    return blueprint


# 示例使用
if __name__ == "__main__":
    bp = build_five_act_blueprint("The Fall of Trust", theme="Betrayal and Redemption")
    for p in bp.phases:
        print(f"{p.phase_id} | {p.phase_type} → {p.expected_function} @ {p.constraints}")

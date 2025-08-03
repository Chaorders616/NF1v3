# blueprint_generator.py - 多结构蓝图生成器（支持 HeroJourney / Tragedy / Mystery 等）

from story_blueprint_system import StoryBlueprint


def build_blueprint(template: str, title: str, theme: str = "Transformation") -> StoryBlueprint:
    blueprint = StoryBlueprint(title=title, theme=theme, structure_type=template)

    if template == "HeroJourney":
        blueprint.add_phase("HJ1", "Ordinary World", "build_trust", {"setting": "home"})
        blueprint.add_phase("HJ2", "Call to Adventure", "initiate_conflict")
        blueprint.add_phase("HJ3", "Refusal", "express_vulnerability")
        blueprint.add_phase("HJ4", "Crossing the Threshold", "raise_stakes")
        blueprint.add_phase("HJ5", "Ordeal", "reveal_secret")
        blueprint.add_phase("HJ6", "Reward", "reframe_goal")
        blueprint.add_phase("HJ7", "Return", "resolve_dispute")

    elif template == "Tragedy":
        blueprint.add_phase("TR1", "Setup", "build_trust")
        blueprint.add_phase("TR2", "Flaw Emerges", "shake_trust")
        blueprint.add_phase("TR3", "Descent", "initiate_conflict")
        blueprint.add_phase("TR4", "Collapse", "raise_stakes")
        blueprint.add_phase("TR5", "Consequences", "reveal_secret")
        blueprint.add_phase("TR6", "Final Fall", "emotional_reckoning")

    elif template == "Mystery":
        blueprint.add_phase("MY1", "Crime Scene", "build_emotion", {"setting": "alley"})
        blueprint.add_phase("MY2", "Investigation Begins", "initiate_conflict")
        blueprint.add_phase("MY3", "Red Herrings", "sustain_opposition")
        blueprint.add_phase("MY4", "Breakthrough", "reveal_secret")
        blueprint.add_phase("MY5", "Twist", "shift_perspective")
        blueprint.add_phase("MY6", "Confrontation", "raise_stakes")
        blueprint.add_phase("MY7", "Resolution", "resolve_dispute")

    else:
        raise ValueError(f"Unsupported blueprint template: {template}")

    return blueprint

from nf1_v3_core.clip_forge_v2 import generate_clips_from_roles

PHASE_GRAPH = [
    {"type": "Introduction", "duration": 1, "intended_shift": "A is unaware", "setting": "Office"},
    {"type": "Escalation", "duration": 2, "intended_shift": "A becomes suspicious", "setting": "Warehouse"},
    {"type": "Confrontation", "duration": 3, "intended_shift": "A accuses B openly", "setting": "Interrogation room"},
    {"type": "Collapse", "duration": 2, "intended_shift": "A loses control", "setting": "Back alley"}
]

def generate_story_structure(role_dict):
    """
    输入角色表，按固定剧情图谱生成多个 Phase → 多个 Clip。
    返回结构化剧情流。
    """
    story = []
    for phase in PHASE_GRAPH:
        phase_data = {
            "phase": phase,
            "clips": generate_clips_from_roles(phase, role_dict)
        }
        story.append(phase_data)
    return story


def summarize_structure(story):
    """
    快速打印故事结构（Phase + Clip Intent）
    """
    for idx, phase in enumerate(story):
        print(f"\n=== Phase {idx+1}: {phase['phase']['type']} ===")
        for clip in phase["clips"]:
            print("-", clip["intent"])

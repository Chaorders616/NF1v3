import pytest

from phase_engine import generate_story_structure
from story_runner import run_story_execution

def test_run_execution_basic_fields():
    result = run_story_execution()

    # 检查关键字段都存在
    assert "script" in result
    assert "hook_analysis" in result
    assert "structure_blueprints" in result
    assert isinstance(result["raw_clips"], list)
    assert len(result["raw_clips"]) > 0

class Role:
    def __init__(self, name, traits, beliefs, emotion_state, intent_bias):
        self.name = name
        self.trait_profile = traits            # 角色性格维度，如：疑心/冷静/虚荣/强迫
        self.belief_map = beliefs              # 世界认知图谱，如：“忠诚高于自由”
        self.emotion_vector = emotion_state    # 当前情绪状态，如：{"anger": 2, "guilt": 0}
        self.intent_bias = intent_bias         # 行动动机偏向，如：“优先保护自己”

    def get_emotion_hint(self):
        # 根据当前情绪状态返回文字提示
        dominant = max(self.emotion_vector.items(), key=lambda x: x[1])[0]
        return f"{self.name} is currently dominated by {dominant}."

    def get_trait_hint(self):
        # 返回个性影响生成倾向
        top_traits = ", ".join([k for k, v in self.trait_profile.items() if v >= 3])
        return f"{self.name} tends to act based on traits: {top_traits}."

    def get_belief_hint(self):
        # 返回一个价值观声明
        if not self.belief_map:
            return ""
        return f"{self.name} believes that {self.belief_map[0]}."

    def describe_state(self):
        return (
            self.get_trait_hint() + " " +
            self.get_emotion_hint() + " " +
            self.get_belief_hint()
        )
    
    def __str__(self):
        return (f"Role(name={self.name}, "
                f"trait_profile={self.trait_profile}, "
                f"belief_map={self.belief_map}, "
                f"emotion_vector={self.emotion_vector}, "
                f"intent_bias={self.intent_bias})")


# 示例角色注册（后续应由角色库管理）
def get_sample_roles():
    A = Role(
        name="A",
        traits={"suspicious": 3, "impulsive": 2},
        beliefs=["betrayal must be punished"],
        emotion_state={"anger": 3, "guilt": 0},
        intent_bias="revenge-oriented"
    )

    B = Role(
        name="B",
        traits={"guilty": 3, "self-defensive": 2},
        beliefs=["survival sometimes requires compromise"],
        emotion_state={"anger": 1, "guilt": 3},
        intent_bias="avoidance"
    )

    return {"A": A, "B": B}

roles = get_sample_roles()
story_structure = generate_story_structure(roles)

print(story_structure)

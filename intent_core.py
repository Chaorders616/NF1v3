"""
IntentCore: 叙事意图核心
StoryThemeManager: 主旨张力控制器
用于控制每段生成是否紧贴核心表达意图，是否围绕主线主题发展
"""

# Narrator's Will
INTENT_CORE = {
    "will_id": "core_betrayal_redemption",
    "motivation": "表达信任被打破后的愤怒与试图修复的徒劳",
    "bias_rules": {
        "clip_selection": "优先矛盾升级与认知反差",
        "character_growth": "允许愤怒转化为冷静后的痛悟",
        "style": "压抑+断裂+反复确认"
    },
    "meta_goal": "让读者体会到人性中的悔恨比愤怒更可怕",
    "control_level": "medium",
    "max_jump_ratio": 0.2,
    "monitor_threshold": 0.7
}


# 显性主题控制器（用于约束 Clip 的情绪/行为是否贴合命题）
STORY_THEME_MANAGER = {
    "core_theme": "背叛之后，没有人能真正原谅",
    "motifs": ["愧疚", "试图修复", "道歉失效", "崩溃后的冷静"],
    "structural_embeddings": {
        "start": "不安与回避",
        "mid": "暴露冲突 + 情绪爆发",
        "end": "表面平静 + 情感断裂"
    },
    "flexible_mode": True,
    "secondary_structures": {
        "mid": ["愤怒反复", "否认失败", "愧疚成瘾"],
        "end": ["表象修复", "冷静压抑", "彻底断绝"]
    }
}


def theme_prompt_prefix(phase_type):
    """
    根据当前 Phase 返回一段叙事意图提示，作为 Prompt 头部添加项
    """
    embedding = STORY_THEME_MANAGER["structural_embeddings"].get(phase_type.lower(), "")
    motifs = ", ".join(STORY_THEME_MANAGER.get("motifs", []))
    return f"This scene should reflect: {embedding}. Key motifs include: {motifs}.\n"


def apply_intent_control(prompt_text, phase_type):
    """
    将当前 phase 的主题/意图注入到 prompt 中，增强全局一致性
    """
    prefix = theme_prompt_prefix(phase_type)
    return prefix + prompt_text

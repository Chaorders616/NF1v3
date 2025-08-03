def build_clip(clip, role_dict=None):
    """
    构造结构描述文本，加入角色行为偏好
    """
    intent = clip.get("intent", "")
    participants = ", ".join(clip.get("participants", []))
    emotion = ", ".join([f"{k}: {v}" for k, v in clip.get("emotion_shift", {}).items()])
    setting = clip.get("setting", "an unknown location")

    role_notes = ""
    if role_dict:
        for name in clip.get("participants", []):
            role_notes += role_dict[name].describe_state() + "\n"

    return (
        f"Scene in {setting}. Participants: {participants}. "
        f"Intent: {intent}. Emotional shift: {emotion}.\n"
        f"Character notes:\n{role_notes}"
    )

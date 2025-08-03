
def format_as_script(clips):
    """
    将 Clip 序列格式化为剧本对白格式。
    """
    output = []
    for i, clip in enumerate(clips):
        setting = clip.get("setting", "Unknown")
        output.append(f"\n# Scene {i+1} - Location: {setting}")
        intent = clip.get("intent", "")
        output.append(f"// Intent: {intent}")

        # 情绪变动提示
        shift = clip.get("emotion_shift", {})
        for role, emotion in shift.items():
            output.append(f"[{role} emotion shift → {emotion}]")

        # 占位对话生成（可替换为模型生成文本）
        a, b = clip.get("participants", ["A", "B"])
        output += [
            f"{a.upper()}: What are you hiding, {b}?",
            f"{b.upper()}: I... I don't know what you mean.",
            f"{a.upper()}: Don't lie to me!"
        ]
    return "\n".join(output)


def format_as_subtitles(clips):
    """
    将 Clip 序列格式化为配音字幕格式。
    每段输出为“角色名 + 对白 + 节奏标记（可扩展为时间轴）”。
    """
    output = []
    counter = 1
    for clip in clips:
        for line in generate_mock_dialogue(clip):
            output.append(f"[{counter}] {line}")
            counter += 1
    return "\n".join(output)


def format_as_storyboard(clips):
    """
    将 Clip 转换为分镜板结构：包含镜头设定、情绪焦点、角色位置建议。
    """
    scenes = []
    for i, clip in enumerate(clips):
        scene = {
            "scene_id": i+1,
            "location": clip.get("setting", "Unknown"),
            "intent": clip.get("intent", ""),
            "participants": clip.get("participants", []),
            "camera": "medium shot with slow zoom",
            "emotion_focus": clip.get("emotion_shift", {}),
            "lighting": "low-key lighting with sharp contrasts"
        }
        scenes.append(scene)
    return scenes


def generate_mock_dialogue(clip):
    """
    简易对话生成（占位用）
    """
    a, b = clip.get("participants", ["A", "B"])
    return [
        f"{a.upper()}: So it's true.",
        f"{b.upper()}: I didn't mean for it to happen.",
        f"{a.upper()}: Then why did you do it?"
    ]

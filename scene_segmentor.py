# scene_segmentor.py

from model_executor import run_gpt
from typing import List, Dict

def segment_scene_into_clips(scene_text: str) -> List[Dict]:
    """
    输入自然语言场景草稿，输出结构化 Clip 列表。
    每个 clip 包含 intent, conflict 状态, emotion shift 等结构字段。
    """
    prompt = f"""
你是一个剧本结构分析师。请将以下自然语言描述的场景，拆解为多个 clip 单元。
每个单元应具备以下字段：
- intent: 这段剧情的核心目的（如揭露、转折、情绪爆发、决定）
- conflict: 是否存在对抗冲突？如有，是什么类型（质疑、威胁、暴力、心理战等）？
- suggested_prompt: 建议用于生成该 clip 的英文 prompt
- optional: 可加入 location, emotion_shift, who, action

请以 JSON 数组格式返回。以下是场景文本：
===
{scene_text}
===
    """

    response = run_gpt(prompt)
    try:
        return eval(response.strip())  # 可替换为 json.loads 取决于模型输出风格
    except:
        return [{"error": "Parsing failed", "raw": response}]

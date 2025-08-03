# blueprint_editor.py（集成自上层场景拆解器）

from model_executor import run_gpt
from typing import List, Dict
from scene_segmentor import segment_scene_into_clips

def extract_blueprint_from_clips(scored_clips: List[Dict]) -> dict:
    """
    从结构评分高的 clip 序列中提炼蓝图结构。
    每个 clip 应含字段: {'score': int, 'clip': str}
    """
    top_clips = [c['clip'] for c in scored_clips if c.get('score', 0) >= 7]
    if not top_clips:
        return {"error": "No strong clips to extract blueprint from."}

    prompt = f"""
你是一位剧情结构专家，请根据以下高质量片段，尝试提取一个剧情蓝图草图。
你应返回 JSON 格式结构如下：
{
  "name": "蓝图建议名称",
  "phases": [
    {"name": "阶段名", "description": "该阶段的剧情目的或功能"},
    ...
  ]
}

=== 高质量片段 ===
{chr(10).join(top_clips)}
    """

    response = run_gpt(prompt)
    try:
        return eval(response.strip())
    except:
        return {"error": "Blueprint extraction failed."}


def extract_clips_from_scene(scene_text: str) -> List[Dict]:
    """
    上层调用接口：将自然语言场景 → 多 Clip
    后续可直接送入 ClipForge
    """
    return segment_scene_into_clips(scene_text)

from model_executor import run_gpt

def audit_against_blueprint(clips: list, blueprint: dict) -> dict:
    """
    比较当前剧本片段与 blueprint 的结构阶段匹配情况。
    返回结构：
    {
        "blueprint_coverage": [...],
        "missing_components": [...],
        "blueprint_match_score": 0-10
    }
    """
    prompt = f"""
你是一个剧本结构分析专家。
请分析以下剧本片段序列与所给蓝图结构的拟合度。

输出要求：JSON 格式，包含：
- blueprint_coverage: 哪些阶段/节点已覆盖
- missing_components: 哪些结构槽位尚未体现
- blueprint_match_score: 匹配度评分（0-10）

=== 剧本片段 ===
{chr(10).join(clips)}

=== 蓝图结构（JSON） ===
{blueprint}
"""

    response = run_gpt(prompt)
    try:
        return eval(response.strip())
    except:
        return {
            "blueprint_coverage": [],
            "missing_components": [],
            "blueprint_match_score": 0
        }
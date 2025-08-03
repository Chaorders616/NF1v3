## nf1_v3_core/structure_blueprints.py
"""
StructureBlueprintSystem: 提供剧情结构模板定义 + 匹配评分 + 推荐改写逻辑
"""

from typing import Dict, List

from model_executor import run_gpt

# 示例结构蓝图（未来可扩展为数据库或用户自定义）
DEFAULT_BLUEPRINTS = [
    {
        "name": "Classic Conflict Curve",
        "phases": ["Setup", "Inciting Incident", "Rising Tension", "Climax", "Resolution"],
        "min_clips": 5,
        "desc": "传统五幕剧结构，适用于单线剧情发展。"
    },
    {
        "name": "Reversal Mystery",
        "phases": ["Normality", "Disturbance", "Discovery", "False Truth", "Twist Reveal"],
        "min_clips": 5,
        "desc": "适用于悬疑与反转型剧情。"
    },
    {
        "name": "Emotional Spiral",
        "phases": ["Hope", "Doubt", "Breakdown", "Confrontation", "Catharsis"],
        "min_clips": 5,
        "desc": "强调情绪起伏与角色转变，适用于心理剧与感情冲突。"
    }
]

def extract_phase_names(raw_clips: List[Dict]) -> List[str]:
    return [clip.get("phase_type", "?") for clip in raw_clips if clip.get("phase_type")]

def match_structure(phases: List[str], blueprint: Dict) -> Dict:
    score = 0
    matched = []
    for p in blueprint["phases"]:
        if p in phases:
            matched.append(p)
            score += 1
    coverage = round(score / len(blueprint["phases"]), 2)
    return {
        "blueprint": blueprint["name"],
        "matched": matched,
        "total_required": blueprint["phases"],
        "coverage": coverage,
        "desc": blueprint["desc"]
    }

def evaluate_all_blueprints(raw_clips: List[Dict]) -> List[Dict]:
    phases = extract_phase_names(raw_clips)
    return [match_structure(phases, bp) for bp in DEFAULT_BLUEPRINTS]

def suggest_missing_structure_additions(blueprints):
    suggestions = []
    for bp in blueprints:
        missing = [p for p in bp["total_required"] if p not in bp["matched"]]
        if missing:
            prompt = f"""
                Blueprint: {bp['blueprint']}
                Missing phases: {missing}

                Write a suggestion for how to insert a new scene that fulfills the missing structure parts: {', '.join(missing)}. Focus on tone, role dynamics, and dramatic purpose.
                """
            suggestion = run_gpt(prompt).strip()
            suggestions.append({
                "blueprint": bp["blueprint"],
                "missing_phases": missing,
                "suggestion": suggestion
            })
    return suggestions

# 示例运行：
if __name__ == "__main__":
    sample_clips = [
        {"phase_type": "Setup"},
        {"phase_type": "Inciting Incident"},
        {"phase_type": "Rising Tension"},
        {"phase_type": "Climax"},
        {"phase_type": "Resolution"},
    ]
    results = evaluate_all_blueprints(sample_clips)
    for r in results:
        print(f"\nBlueprint: {r['blueprint']}\nMatched: {r['matched']}\nCoverage: {r['coverage']} → {r['desc']}")

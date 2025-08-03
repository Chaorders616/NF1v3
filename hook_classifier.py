# hook_classifier.py (v2) - 含 function_hierarchy, intent_signals with weight, structure_constraints

from model_executor import run_gpt
from hook_schema import narrative_function_hierarchy, intent_signal_schema
from typing import Dict
import json

def classify_hook_text(text: str, context: str = "") -> Dict:
    """
    对一个候选句子进行结构性hook分析，输出function_hierarchy, intent_signals, structure_constraints
    """
    function_prompt_list = "\n".join(
        [f"- {group}: {', '.join(funcs)}" for group, funcs in narrative_function_hierarchy.items()]
    )

    signal_fields = ", ".join(intent_signal_schema.keys())

    prompt = f"""
你是一个叙事结构分析专家，请分析以下句子是否可以作为结构钩子（Hook），并提取其结构意图。

句子：\n{text}

上下文片段：\n{context}

请输出以下字段：
- is_hook: 是否为结构钩子（是/否）
- narrative_function: 所属的具体功能（从以下列表中选一个）
{function_prompt_list}
- function_hierarchy: 所属功能路径（如 ["build_emotion", "raise_emotional_stake"]）
- intent_signals: 语义信号字段及权重，字段包含：{signal_fields}，每项结构为 {{value: str, weight: float}}
- structure_constraints: 包括：
    - expected_resolution_phase（如 Setup / Rising Action / Climax / Resolution）
    - recommended_recall_style（如 emotional_reckoning / direct_confrontation）
    - reversal_conditions: JSON对象，字段包括 probability, trigger[], effect

请用 JSON 格式输出。
"""

    response = run_gpt(prompt)
    try:
        parsed = json.loads(response.strip())
        if isinstance(parsed.get("intent_signals"), list):
            parsed["intent_signals"] = {
                entry["field"]: {"value": entry["value"], "weight": entry["weight"]}
                for entry in parsed["intent_signals"]
                if "field" in entry
    }
        return parsed
    except Exception as e:
        return {
            "is_hook": False,
            "error": f"Failed to parse response: {str(e)}",
            "raw_output": response
        }

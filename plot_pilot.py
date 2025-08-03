# plot_pilot.py

import os
import json
from typing import List, Dict

# 可扩展的蓝图注册表
default_blueprints = {}


def register_blueprint(name: str, structure: List[Dict]):
    """注册一个新的剧情蓝图"""
    default_blueprints[name] = structure


def get_blueprint(name: str) -> List[Dict]:
    """获取指定名称的蓝图结构"""
    return default_blueprints.get(name, [])


def list_blueprint_names() -> List[str]:
    return list(default_blueprints.keys())


def get_all_blueprints() -> Dict[str, List[Dict]]:
    return default_blueprints


# 🔁 支持从 JSON 文件夹动态加载蓝图
BLUEPRINTS_DIR = "blueprints"

def load_blueprints_from_directory(directory: str = BLUEPRINTS_DIR):
    if not os.path.exists(directory):
        return
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        name = filename.replace(".json", "")
                        register_blueprint(name, data)
                except Exception as e:
                    print(f"❌ Failed to load blueprint {filename}: {e}")


# 预设蓝图：经典冲突曲线
register_blueprint("Classic Conflict Curve", [
    {"phase": "Setup", "intent": "Introduce characters and world"},
    {"phase": "Inciting Incident", "intent": "Trigger main conflict"},
    {"phase": "Rising Tension", "intent": "Escalate stakes and dilemmas"},
    {"phase": "Climax", "intent": "Crisis and key decision"},
    {"phase": "Resolution", "intent": "Wrap up consequences and arc"},
])

# 预设蓝图：情绪螺旋结构
register_blueprint("Emotional Spiral", [
    {"phase": "Hope", "intent": "Show motivation or glimpse of better future"},
    {"phase": "Doubt", "intent": "Introduce cracks in belief or relationship"},
    {"phase": "Breakdown", "intent": "Loss, crisis, or collapse moment"},
    {"phase": "Catharsis", "intent": "Emotional release, realization, rebirth"},
])

# 默认使用哪一个蓝图
DEFAULT_BLUEPRINT = "Classic Conflict Curve"


def generate_story_structure(role_list: List[Dict], blueprint_name: str = DEFAULT_BLUEPRINT) -> List[Dict]:
    blueprint = get_blueprint(blueprint_name)
    structure = []
    for p in blueprint:
        structure.append({
            "phase": p,
            "clips": []
        })
    return structure


# 自动初始化时加载自定义蓝图
load_blueprints_from_directory()

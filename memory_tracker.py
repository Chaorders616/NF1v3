"""
MemoryMatrix: 结构化剧情记忆与未解钩子追踪系统
包含：
- event_log：按顺序记录所有事件片段摘要
- hook_queue：所有挂起的伏笔钩子（未被回收）
- recall_log：被回收的钩子清单（已解决）
"""


from datetime import datetime
from typing import List, Dict


class MemoryMatrix:
    def __init__(self):
        self.event_log = []  # 全部事件记录
        self.hooks = []       # 所有注册钩子

    def add_event(self, clip, summary=None, hook_type=None, critical=False):
        event = {
            "clip_id": clip.get("clip_id", "unknown"),
            "text": clip.get("text"),
            "summary": summary or clip.get("summary", ""),
            "hook_type": hook_type or "general",
            "critical": critical,
            "timestamp": self.get_current_time()
        }
        self.event_log.append(event)

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def try_register_and_recall(self, clip: dict, clip_index: int):
        """执行双机制：注册当前钩子，尝试回收已有钩子"""
        hook_text = clip["text"].split("?")[0] + "?" if "?" in clip["text"] else clip["text"][:40] + "..."
        new_hook = {
            "hook_id": f"clip{clip_index}_H1",
            "text": hook_text,
            "origin_clip": clip_index,
            "hook_type": None,
            "strength": 0.0,
            "recalled": False,
            "recall_clip": None
        }
        self.register_hook(new_hook)

        # 尝试回收历史钩子
        prior_hook = self.find_high_priority_hook()
        if prior_hook and prior_hook['text'].lower() in clip['text'].lower():
            self.recall_hook(prior_hook['hook_id'], clip_index)

    def register_hook(self, hook: dict):
        """注册一个钩子，包括其类型、来源、强度等信息"""
        self.hooks.append(hook)

    def recall_hook(self, hook_id: str, clip_index: int):
        """标记指定钩子为已被回收，记录回收位置"""
        for hook in self.hooks:
            if hook['hook_id'] == hook_id:
                hook['recalled'] = True
                hook['recall_clip'] = clip_index
                break

    def list_active_hooks(self) -> List[dict]:
        """列出所有未被回收的钩子"""
        return [h for h in self.hooks if not h.get('recalled', False)]

    def list_all_hooks(self) -> List[dict]:
        return self.hooks

    def find_high_priority_hook(self) -> dict:
        """寻找强度较高、仍未回收的钩子（简化版本）"""
        active_hooks = self.list_active_hooks()
        if not active_hooks:
            return None
        return sorted(active_hooks, key=lambda h: h.get('strength', 0), reverse=True)[0]

    def mark_hook_recalled(self, hook_id: str):
        """旧接口兼容：将钩子标记为回收（不记录位置）"""
        self.recall_hook(hook_id, clip_index=None)

    def get_hooks_for_clip(self, clip_index: int) -> List[dict]:
        """获取某个片段中曾注册的钩子"""
        return [h for h in self.hooks if h.get('origin_clip') == clip_index]

    def try_register_and_recall(self, clip: dict, clip_index: int):
        """执行双机制：注册当前钩子，尝试回收已有钩子"""
        hook_text = clip["text"].split("?")[0] + "?" if "?" in clip["text"] else clip["text"][:40] + "..."
        new_hook = {
            "hook_id": f"clip{clip_index}_H1",
            "text": hook_text,
            "origin_clip": clip_index,
            "hook_type": None,
            "strength": 0.0,
            "recalled": False,
            "recall_clip": None
        }
        self.register_hook(new_hook)

        # 尝试回收历史钩子
        prior_hook = self.find_high_priority_hook()
        if prior_hook and prior_hook['text'].lower() in clip['text'].lower():
            self.recall_hook(prior_hook['hook_id'], clip_index)



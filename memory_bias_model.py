## nf1_v3_core/memory_bias_model.py

"""
MemoryBiasModel：为多角色构建带偏差的记忆系统
每个角色将拥有一份“带立场”的记忆副本，对事件的理解可能不同，
可用于生成不同角色视角的对话 / 冲突 / 自我辩护逻辑。
"""


class MemoryBiasModel:
    def __init__(self, roles):
        self.roles = roles
        self.memory_by_role = {r.name: [] for r in roles.values()}

    def record_event(self, event):
        for role in self.memory_by_role:
            biased_view = self._apply_bias(event, role)
            self.memory_by_role[role].append(biased_view)

    def _apply_bias(self, event, role_name):
        # 简化版偏差模拟逻辑
        base_summary = event["summary"]
        intent = event.get("intent", "")
        if role_name in event.get("participants", []):
            if "accuse" in intent.lower():
                bias = f"Felt unfairly blamed: {base_summary}"
            elif "confess" in intent.lower():
                bias = f"Admitted under pressure: {base_summary}"
            else:
                bias = f"Remembered as intense: {base_summary}"
        else:
            bias = f"Heard from others: {base_summary}"
        return {
            "origin": event,
            "viewpoint": role_name,
            "biased_summary": bias
        }

    def get_memory_for(self, role_name):
        return self.memory_by_role.get(role_name, [])

# 用法示例：
if __name__ == "__main__":
    roles = [
        {"name": "A"},
        {"name": "B"},
        {"name": "C"}
    ]
    model = MemoryBiasModel(roles)

    event = {
        "summary": "B admitted the betrayal",
        "participants": ["A", "B"],
        "intent": "A accuses B"
    }
    model.record_event(event)

    for role in ["A", "B", "C"]:
        print(f"\n--- {role}'s memory ---")
        for item in model.get_memory_for(role):
            print(item["biased_summary"])

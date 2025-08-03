## nf1_v3_core/viewpoint_recaster.py

"""
ViewpointRecaster：角色视角复述生成器 + 认知冲突检测器
从角色偏见记忆出发，生成主观旁白，分析角色之间的认知冲突点（偏差总结）
"""

from model_executor import run_gpt


class ViewpointRecaster:
    def __init__(self):
        self.last_conflicts = []

    def generate_recast(self, role_name, memory_items, tone="defensive", purpose="justify themselves"):
        prompt = self.build_prompt(role_name, memory_items, tone, purpose)
        return run_gpt(prompt)

    def build_prompt(self, role_name, memory_items, tone, purpose):
        mem_list = "\n".join([f"- {m['biased_summary']}" for m in memory_items])
        return f"""
            You are {role_name}. 
            Here are your recollections of recent events:
            {mem_list}

            In a {tone} tone, write a monologue where you try to {purpose}, based only on your memory.
            Avoid mentioning it is a memory. Make it sound real and present.
            """

    def detect_cognitive_conflict(self, memory_by_role):
        """
        接收 MemoryBiasModel.memory_by_role
        分析不同角色间对事件的偏见记忆是否产生认知冲突
        返回冲突摘要列表，并记录在 self.last_conflicts 中供外部访问
        """
        conflict_summary = []
        roles = list(memory_by_role.keys())

        for i in range(len(memory_by_role[roles[0]])):
            summaries = []
            for r in roles:
                mems = memory_by_role[r]
                if i < len(mems):
                    summaries.append((r, mems[i]["biased_summary"]))

            if len(set(s[1] for s in summaries)) > 1:
                conflict_summary.append({
                    "index": i,
                    "views": summaries
                })

        self.last_conflicts = conflict_summary
        return conflict_summary

    def get_last_conflicts(self):
        return self.last_conflicts

def generate_conflict_debate_snippets(conflicts):
    debate_snippets = []
    for conflict in conflicts:
        views = conflict["views"]
        if len(views) < 2:
            continue
        a, a_view = views[0]
        b, b_view = views[1]
        prompt = f"""
            A dialogue scene between {a} and {b}. They argue about what happened:
            {a}: \"{a_view}\"
            {b}: \"{b_view}\"
            Now continue the conversation for 4 more exchanges, emotionally charged and escalating.
            """
        output = run_gpt(prompt)
        debate_snippets.append({
            "index": conflict["index"],
            "roles": [a, b],
            "snippet": output.strip()
        })
    return debate_snippets

def generate_truth_seeking_monologues(biased_memory):
    result = {}
    for role, memories in biased_memory.items():
        prompt = """
            You are {role}, and you are deeply unsure whether your version of past events is true.
            Here are your biased memories:
            {memories}
            Now write an introspective internal monologue as you try to discover the truth.
            You may doubt yourself, recall contradictions, or speculate what others might have meant.
            """.format(
                        role=role,
                        memories="\n".join(f"- {m['biased_summary']}" for m in memories)
                    )
        monologue = run_gpt(prompt)
        result[role] = monologue.strip()
    return result

def generate_reframe_monologues(biased_memory):
    result = {}
    for role, memories in biased_memory.items():
        mem_list = "\n".join(f"- {m['biased_summary']}" for m in memories)
        biased_prompt = f"You are {role}. Based on the following memories, write a confident monologue presenting your side:\n{mem_list}"
        truth_prompt = f"You are {role}. You're now doubting the truth of the following memories:\n{mem_list}\nNow write a monologue seeking what really happened."

        biased = run_gpt(biased_prompt).strip()
        truth = run_gpt(truth_prompt).strip()
        result[role] = {
            "biased_version": biased,
            "truth_doubt_version": truth
        }
    return result



def reconcile_conflicting_memories(conflicts):
    reconciled = []
    for conflict in conflicts:
        if len(conflict["views"]) < 2:
            continue
        views_text = "\n".join([f"{r}: {v}" for r, v in conflict["views"]])
        prompt = f"""
            The following characters have conflicting memories of the same event:
            {views_text}

            Write a scene in which they gradually reconcile these differences. They may recall new facts, confront each other, or uncover a missing clue. End with a shared understanding or consensus.
            """
        scene = run_gpt(prompt).strip()
        reconciled.append({
            "index": conflict["index"],
            "roles": [r for r, _ in conflict["views"]],
            "resolution_scene": scene
        })
    return reconciled

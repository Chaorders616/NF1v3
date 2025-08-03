## nf1_v3_core/auto_critic.py

"""
AutoCritic 模块：自动评估生成段落的结构质量与叙事一致性
目标是发现：是否符合主旨、情绪节奏是否推进、是否存在结构缺陷或冲突违和。
扩展版加入：对话比例、角色情绪偏差、结构节奏图谱对齐。
新增支持：当评分低于阈值时触发自动重写逻辑。
新增整体结构评分分析：平均分、标准差、弱点段落定位。
新增 Clip 因果图谱生成器：基于事件摘要、钩子与回收关系形成可视化图数据。
新增 HTML 渲染支持：将因果图输出为 vis.js 图形结构。
"""


class AutoCritic:
    def __init__(self, intent_core, theme_manager, rewrite_threshold=0.6):
        self.intent_core = intent_core
        self.theme_manager = theme_manager
        self.rewrite_threshold = rewrite_threshold

    def evaluate_clip(self, clip):
      """
      为单个 Clip 打分，主要评估以下维度：
      - 情绪张力是否存在
      - 是否存在角色意图或转变
      - 是否存在结构落点（例如“反转”或“推进”）
      """
      text = clip.get("text", "")
      score = 0
      notes = []

      if any(word in text.lower() for word in ["but", "however", "yet"]):
          score += 2
          notes.append("结构反转存在")

      if any(word in text.lower() for word in ["realize", "decide", "confess", "reject"]):
          score += 2
          notes.append("角色意图清晰或出现变化")

      if any(em in text.lower() for em in ["guilt", "rage", "fear", "shame", "hope"]):
          score += 2
          notes.append("情绪张力良好")

      if len(text.split()) < 30:
          score -= 1
          notes.append("内容可能偏短")

      rewrite_required = score < 4
      return score, notes, rewrite_required

    def evaluate_full_story(self, clips):
        # ... 保持不变 ...
        pass

    def build_causal_graph(self, raw_clips):
      nodes = []
      edges = []

      for i, clip in enumerate(raw_clips):
          node_id = i + 1
          summary = clip.get("summary", "")
          scene = clip.get("scene", "")
          label = f"{node_id}: {summary[:80]}"  # 限制长度
          nodes.append({
              "id": node_id,
              "label": label,
              "shape": "box",
              "color": "#cceeff"
          })

          # 默认顺序边（弱因果）
          if i > 0:
              edges.append({
                  "from": i,
                  "to": node_id,
                  "label": "then",
                  "arrows": "to"
              })

          # ✅ 强因果：如果这个 clip 回收了钩子
          if "hook_resolved" in clip:
              for j, c2 in enumerate(raw_clips):
                  if c2.get("hook_id") == clip["hook_resolved"]:
                      edges.append({
                          "from": j + 1,
                          "to": node_id,
                          "label": "hook_recall",
                          "color": "red",
                          "dashes": True,
                          "arrows": "to"
                      })

          # ✅ 高级：情绪/意图跳跃也可作为边条件
      return {"nodes": nodes, "edges": edges}

    def export_visjs_html(self, graph_data, output_file="causal_graph.html"):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
  <title>NF1因果结构图</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
  <style>#mynetwork { width: 100%; height: 90vh; border: 1px solid lightgray; }</style>
</head>
<body>
  <h2>NF1 因果结构图谱</h2>
  <div id="mynetwork"></div>
  <script>
    const nodes = new vis.DataSet(""")
            f.write(str(graph_data["nodes"]))
            f.write(""");
    const edges = new vis.DataSet(""")
            f.write(str(graph_data["edges"]))
            f.write(""");
    const container = document.getElementById("mynetwork");
    const data = { nodes: nodes, edges: edges };
    const options = {
      layout: { hierarchical: { direction: "UD" } },
      edges: { arrows: "to", color: "gray" },
      nodes: { shape: "box", color: "lightblue" }
    };
    new vis.Network(container, data, options);
  </script>
</body>
</html>
""")

# 用法示例（节选）：
if __name__ == "__main__":
    from intent_core import INTENT_CORE, STORY_THEME_MANAGER
    from story_runner import run_story_execution

    critic = AutoCritic(INTENT_CORE, STORY_THEME_MANAGER)
    output = run_story_execution()

    graph = critic.build_causal_graph(output["raw_clips"])
    critic.export_visjs_html(graph)
    print("Causal graph exported to causal_graph.html")

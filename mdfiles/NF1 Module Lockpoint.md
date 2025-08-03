# NF1 V3 系统级正式止损锁定线

日期：2025-07-29

---

## 【当前版本进展】

当前版本已实现：

1. **首次 AI Prompt 生成链路可以成功运行（MVP 的内核）**,运行结果见: `首次生成链接跑通结果.md`
2. 支持 Clip 装配的 Prompt 工程化生成、敏感词解决、编辑重写
3. 支持 MemoryMatrix 重要事件记录 + hook 分析、强化推理
4. 已实现自动化分段 clip 生成，并进行合理分数结构
5. 加入 AutoCritic 评分系统，支持 clip 评分和重写
6. 已创建 plot\_pilot.py ，支持剪裁后放入 "戏情蓝图"结构

---

## 【正式锁定的内核模块】

### 1. Prompt 工程

* 构造角色、场景、情绪、效果结构
* 展开：新增 PromptAssembler 模块

### 2. ClipForge

* 根据戏情段落解析 intent ，生成初始 clip
* 展开：后期将开始支持按 intent 检查并重构 prompt

### 3. StoryRunner

* 展开 clip 执行进程：分阶段 prompt 生成 - 评分 - 重写
* 合并为效果输出的结构：

  * raw\_clips
  * subtitle\_text
  * causal\_graph
  * summary hook

### 4. MemoryMatrix

* 记录重要情节和 hook
* 标记操作：add\_event，recall\_hook，register\_hook

### 5. AutoCritic

* 单元 clip 评分 + 全剧构造评估
* 后期展开：增加 "责性循环" 或 "行为合理性分析"

### 6. PlotPilot (剧情蓝图)

* 蓝图定义规范和 intent
* 支持从 blueprints/文件加载用户自定义蓝图

---

## 【已短期计划展开模块】

1. **clip 构造时提前进行 intent 分析和 prompt 扩充**
2. 开启 **StoryBlueprintGuidance** 系统：先生成剧情蓝图内容
3. 增强 AutoCritic 结构评分能力，展开 hook-structure 合理性分析
4. 实现 "Scene Description -> Clip 分解" 的场景分割器

---

## 【正在进行的积本设计】

* 构造统一的 style\_profiles.json / impact\_profiles.json / blueprint 仓库
* 规范化 story\_structure 控制形式
* 提出 "无 AI 操作模态下先完成结构"的设计原则

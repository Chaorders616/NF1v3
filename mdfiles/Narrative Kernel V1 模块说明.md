# NarrativeKernel V1 模块说明文档

以下为 NE 核心叙事内核（NarrativeKernel）中各模块功能说明，涵盖其职责、输入输出结构与设计哲学。

---

## 🧠 FiveForcePlanner

**功能：** 提取用户意图，生成五力框架（主题张力核心）

**输入：**

* `user_intent`（文本 / 结构化叙事意图）
* `world_template`（可选：世界观设定）

**输出：**

* `theme`：作品主旨/命题张力
* `conflict_core`：核心对立点（主角 vs 势力/世界）
* `character_arcs`：人物成长线基础走向
* `background_tension`：社会环境暗线（如失控、崩塌）
* `hook_density`：计划钩子密度节奏（多少段落内有爆点）

**设计哲学：**

* 将用户“模糊情节愿望”转化为结构动力五力
* 定义“写什么 + 冲突源头 + 人物演化”的三维出发点

---

## 📐 BlueprintEngine

**功能：** 基于五力结构构建叙事蓝图（剧本大纲）

**输入：**

* `five_forces`：由 FiveForcePlanner 输出的五力要素

**输出：**

* `narrative_blueprint`：章节级结构图（如三幕/五段/主线支线）
* `sequence_outline`：关键事件顺序（含爆点节点）

**设计哲学：**

* 避免“生成剧本从第一句写起”，先建框架后填充
* 以“张力/角色/节奏”为原则生成结构，不死跟模板

---

## 🔨 ClipForge

**功能：** 将蓝图拆解为 Clip（段落单元），并生成对白、情绪、视觉意象

**输入：**

* `narrative_blueprint`（章节结构）
* `hook_config`（钩子计划）

**输出：**

* `clip_units`：具备目标、节奏、角色意图的最小叙事单元
* `dialogue_blocks`：情节对白（含语气与暗示）
* `emotion_flows`：Clip 内情绪张力轨迹

**设计哲学：**

* 每个 Clip 是“叙事胶囊”，可独立使用也可拼接成长结构
* 实现“钩子驱动”与“结构一致性”的融合写作

---

## 🎣 HookEngine

**功能：** 检测或生成钩子结构，定位爆点张力

**输入：**

* `clip_units`（段落）

**输出：**

* `hook_map`：钩子类型、位置、节奏图谱
* `hook_peak_timing`：高潮/反转/冲击出现时机

**设计哲学：**

* 钩子非模板化，而是“情绪曲线下的爆点自然生成”
* 同时支持评估已有结构的钩子强度，进行提醒或增补

---

## 🛡️ TensionProxyLayer

**功能：** 在不影响结构的前提下，对可能触发模型审查的语言进行包装或代理

**输入：**

* `dialogue_blocks`（原始对白）

**输出：**

* `sanitized_script`（带语义但已脱敏的对白结构）

**设计哲学：**

* 通过“结构代词 + 暗示语气 + 情绪链”保持张力但规避敏感词
* 保证生成系统的通用性、合法性与后续执行成功率

---

## 🧾 PromptCompiler

**功能：** 将结构化内容转化为生成模型可消费的 Prompt

**输入：**

* `clip_units`
* `sanitized_script`

**输出：**

* `ScenePromptUnit`（包括镜头语言、动作描述、情绪、对话）

**设计哲学：**

* 专为 SoraLite、图像生成、播客TTS 等多模态生成器输出准备
* 将结构语义化，不用一句句 prompt 拼接

---

## 🎛️ SceneCommandInterface

**功能：** 输出最终结构指令，交由外部多模态执行系统处理

**输入：**

* `ScenePromptUnit`

**输出目标：**

* `text_output`（文字剧本）
* `tts_output`（音频对白）
* `image_gen`（视觉帧画）
* `video_pipeline`（镜头序列）

**设计哲学：**

* NE 不亲自生成模态内容，而是给出“导演意图指令包”
* 保证每一镜头输出都具有结构可溯性与节奏内在一致性

# NE 未来优势战略规划

> 更新时间：2025-08-01  
> 版本：vNext 战略框架草案（待执行）

---

## 🧭 核心战略定位

### 🔮 新范式认知
- 随着百万Token模型普及，AI生成将进入“全结构输入 → 自洽展开 → 回流验证”的阶段。
- NE 不再只是结构转镜头，而是承担结构控制、执行映射、内容优化的三重中枢角色。

### 🎯 NE 的优势角色（未来三重职能）
1. **结构意图的视觉执行官**
2. **叙事策略的上下文映射器**
3. **全局控制目标与多模态执行之间的桥梁层**

---

## 🧠 结构重构核心策略

### ✅ 1. GlobalStructurePack（GSP）统一结构输入格式

用于百万Token模型 ingest 的完整结构语义包：

```json
{
  "title": "逆光而行",
  "structure_type": "非线性",
  "phases": [...],
  "hooks": [...],
  "emotion_curve": [...],
  "characters": [...],
  "worldstate": {...},
  "recall_targets": [...],
  "style_directives": {...}
}
```

---

### ✅ 2. 执行引擎双通道设计

| 执行模式                   | 说明                                           |
|------------------------|----------------------------------------------|
| `stepwise_execution()`     | 逐阶段、逐Clip推进，适配弱模型、强调控制力               |
| `global_infer_and_align()` | 一次性输入 GSP → 输出剧本 → 回流校验结构命中率 → 标记修复点 |

---

### ✅ 3. StructureAlignmentMonitor（SAM）结构执行追踪器

- Hook回忆率分析
- 情绪曲线偏移检测
- 阶段缺失/偏移提示
- 全局结构命中评分（alignment_score）

---

### ✅ 4. ScenePromptPack 模块

统一管理一段 Clip 的全部执行提示：

```json
{
  "clip_id": "scene_4a",
  "text_summary": "...",
  "visual_prompt": "...",
  "style_tags": ["moody", "film noir"],
  "tts_voice": "female_angry_low",
  "bgm_mood": "tense"
}
```

---

### ✅ 5. PlatformFlavorAdapter

输出多平台版本：抖音、Runway、可灵等。结构一致，节奏重组。

---

### ✅ 6. StructurePromptCompiler

将 GSP → 拆分为多类 Prompt，包括：
- 角色指令 Prompt
- 情绪转折 Prompt
- 镜头风格 Prompt
- 画面修复 Prompt

---

## 🧠 新能力扩展：结构优化器系统

长上下文将 NE 升级为成文内容的“结构医生”

### 典型任务
- 小说章节结构点评
- 编剧脚本结构修订建议
- 剪辑节奏张力分析
- 二创内容一致性校验

### 关键模块

| 模块名                    | 职责                                      |
|------------------------|-----------------------------------------|
| StructureReverseMapper | 从文本反推 GSP 结构                         |
| HookEffectivenessAnalyzer | 分析已埋Hook是否被回应                         |
| EmotionCurveExtractor  | 抽取文本张力曲线并对比理想轨迹                   |
| SceneMergeRecommender | 提出结构优化建议（剪辑顺序、合并等）               |
| StructureCriticGPT     | 输出总结建议：“第3段张力低、第7段未呼应初始冲突”等     |

---

## 🔁 使用模式对照表

| 模式                       | 用途                      |
|--------------------------|---------------------------|
| stepwise_control         | 精准控制，适配短剧和教学模式         |
| global_infer_then_slice  | 快速产出长文本，如小说/多镜头剧本     |
| hybrid_mode              | 全结构输入 + 局部片段修复补全       |
| optimize_existing_content | 对已有作品进行结构提取与优化建议生成 |

---

## 🧩 NE 模块职能矩阵（vNext）

| 模块名                      | 类型     | 职责概要                             |
|--------------------------|--------|----------------------------------|
| GlobalStructurePack       | 输入结构 | NF→NE核心中间层结构定义                 |
| ScenePromptPack           | 输出包   | 单Clip多模态执行包                    |
| StructureAlignmentMonitor | 工具集   | 对比GSP与实际输出，评估结构偏差            |
| StructurePromptCompiler   | Prompt | 根据结构拼装执行提示词                   |
| PlatformFlavorAdapter     | 输出器   | 多平台结构输出                        |
| StructureReverseMapper    | 分析器   | 结构优化器核心模块，从文本构造结构并评分        |
| StructureCriticGPT        | 分析器   | 用自然语言输出改进建议                    |

---

## 🚦 推荐落地顺序（建议迭代路线）

1. 定义 GSP 格式规范（字段+示例）
2. 构建 ScenePromptPack 模板化系统
3. 接入双通道执行器（stepwise + global）
4. 实现 StructureAlignmentMonitor 框架
5. 启动 StructureReverseMapper（结构优化器）
6. 拆分 StructurePromptCompiler + 多平台适配器

---

## ✅ 启动模块指令（标准格式）

> 开始模块开发，只需下达以下指令之一：

- “执行 GSP 结构格式定义”
- “启动 ScenePromptPack 构建器”
- “构建结构反向分析器（StructureReverseMapper）”
- “开启结构执行对齐系统（SAM）”
- “进入结构优化器开发阶段”

---
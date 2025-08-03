# NF1 V3 项目结构说明文档

本文档最后更新于2025-07-29, 已不完全适用于最新构建进程.请参考GPT自身记忆 + 文件夹: `nf1_v3_core\mdfiles\`下相关内容.

---

## 📌 0. 项目定位与哲学

* **项目目标**: 构建一套基于结构控制的内容 AI 生成系统。
* **格式思想**:

  * 结构先行，生成从律；
  * 控制边界，可化编的分段、分户、角色主控生成。
  * 质量问题带有问证、评分、重写；
  * 保持更新时线和跨段落进度统一性。  

## 🧱 1. 系统模块概览

| 模块                | 职责           | 关键函数                                    | 状态 |
| ----------------- | ------------ | --------------------------------------- | -- |
| PhaseEngine       | 效果相关的分段/分阶构造 | `generate_story_structure()`            | ✅  |
| ClipForge         | Clip 基本单元生成  | `generate_clips()`, `build_clip()`      | ✅  |
| PromptAssembler   | Prompt 构造/配置 | `assemble_prompt()`                     | ✅  |
| MemoryMatrix      | 记忆注册/钩子处理    | `register_hook()`, `recall_hook()`      | ✅  |
| HookEvaluator     | 钩子分析/链接性检测   | `annotate_hooks_with_type_and_weight()` | ✅  |
| AutoCritic        | 内容质量评分器      | `evaluate_clip()`                       | ✅  |
| BlueprintMatcher  | 效果结构对比器      | `evaluate_all_blueprints()`             | ⏳  |
| ViewpointRecaster | 角色心态重构/绝对证诀  | `generate_conflict_debate_snippets()`   | ✅  |
| story\_runner.py  | 引擎/总结/输出     | `run_story_execution()`                 | ✅  |

## 🔁 2. 内容生成流程

**进入之前：先构造结构，后启用AI**

```
用户意图 → 角色配置 → 效果结构 → 分段Clip构造
→ 构造Prompt → AI生成Clip → 总结 + 钩子注册 + 评分 + 重写 → 内容集成
```

## 🧠 3. 控制策略

* **Prompt 控制**: 分段Prompt配合角色、情感、格式要求
* **评分控制**: 质量<7规则重写，论证输出 critic\_notes
* **钩子控制**: register/recalled/强化重写/异常检测

## 📂 4. 文件结构

* `story_runner.py` 主逻辑
* `phase_engine.py` 分阶
* `clip_forge.py` 创clip
* `style_compiler.py` 风格规则
* `hook_evaluator.py` 钩子跨段求解
* `auto_critic.py` 内容级别化判断

## ⚙️ 5. 已知问题 & 重点开发方向

* Blueprint结构对齐没有真正关联到分阶生成模块
* Memory钩子未完全分类化，hook\_type处理逻辑没有打通
* Viewpoint重构只能输出 monologue 文本，未用于实际clip重构
* Hook与\uBlueprint未实现通信（e.g. clip错过了Blueprint成员场景）

## 📜 6. Roadmap

* 第一阶段 MVP: 效果结构 + prompt 控制 ✅
* 第二阶段: 质量重写和钩子连续 ✅
* 第三阶段: blueprint-角色联动效果装配
* 第四阶段: UI/自动化/互动开发

---

##  7. 项目环境信息:

### 项目环境
Windows 10,VScode 虚拟环境(.venv),Clash(Rule mode)

### 项目文件绝对路径
`F:\Code\Python\MyProjects\NF1v3\nf1_v3_core`

### API信息
```
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-008f***1b"
)
```

## 8. 其他说明文件:

所在文件夹: `nf1_v3_core\mdfiles\`;




# NE 世界观生成器 WorldModel V1 设计实体

方向：为了支持复杂剧本、多模态输出和反结构结构，NE 需要建立一套“世界观体系”，用来定义 Five Forces 的运行规则和解释场景

---

## 一、WorldModel 在 NE 中的位置

| 成分                    | 简述                                        |
| --------------------- | ----------------------------------------- |
| 世界场景 setting          | 故事为何发生在这里？时间、地点、积累历史                      |
| 社会规则 rules            | 人物可以怎么行动，当场的社会/物理/情感规则是什么                 |
| 情绪该有形态 affect grammar | 观众应该怎样感知情绪？是前按钮的注意力，还是原生思维？               |
| 价值形成 logic            | “好、坏、正义、罪恶” 这类概念是否存在？是被证明，还是一种异质、手段、并行规则？ |
| 主题规范 theme scope      | 这种世界下，可以进行什么样式的主题探究？那些主题会被识为不合理或失效？       |

---

## 二、WorldModel 格式建议 (JSON Schema 分析)

```json
{
  "world_id": "cyberpunk_redemption_v1",
  "setting": {
    "time": "2167 AD",
    "location": "Neo-Osaka Upper Rings",
    "background": "Post-corp collapse techno-feudalist citystate"
  },
  "rules": {
    "memory_editing": true,
    "biometric_surveillance": true,
    "death": "irreversible",
    "emotion_display": "quantified"
  },
  "emotion_grammar": {
    "permitted_emotions": ["guilt", "ecstasy", "shame", "desire"],
    "expression_modes": ["neural signature", "light tattoos"]
  },
  "value_model": {
    "justice": "algorithmic",
    "loyalty": "genetic contract",
    "truth": "subjective",
    "family": "economic pod"
  },
  "theme_scope": {
    "permitted": ["survival vs identity", "algorithmic ethics", "corporate godhood"],
    "forbidden": ["rural nostalgia", "traditional honor"]
  }
}
```

---

## 三、世界观和 Five Forces 的关系

| Five Forces  | 世界观影响                         |
| ------------ | ----------------------------- |
| 主题 Theme     | 决定“能探讨哪些主题”是有效 / 有影响力的        |
| 角色 Character | 决定人物的行动跟同情义是否合理（例如：不能哭、不能杀人）  |
| 情绪 Emotion   | 决定哪些情感是允许表达、以什么形式进行           |
| 类型 Genre     | 决定所有 blueprint 中是否允许重复/跳离/无结尾 |
| 钩子 Hook      | 决定信息是否能被隐藏？会被怎样的社会机制维系        |

---

## 四、建议扩展

* 建立 WorldTemplateLibrary：为不同剧类存储世界观基础
* 配合 CharacterArchetypeMatrix 根据世界观输出合理角色行为
* 同时配套 PromptScopeLimiter，给 GPT 系列无法输出被禁止主题/情感
* 用于 multi-IP universe 中，符合同一世界的故事自动检测

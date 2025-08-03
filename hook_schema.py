# hook_schema.py - Hook结构功能词典与信号体系定义

# ✅ Hook结构功能分层定义
narrative_function_hierarchy = {
    "build_emotion": [
        "build_trust",
        "shake_trust",
        "express_vulnerability",
        "reaffirm_connection"
    ],
    "drive_conflict": [
        "initiate_conflict",
        "escalate_tension",
        "sustain_opposition",
        "provoke_betrayal"
    ],
    "raise_stakes": [
        "introduce_deadline",
        "reveal_external_pressure",
        "escalate_consequences"
    ],
    "uncover_truth": [
        "reveal_secret",
        "expose_motive",
        "unmask_lie"
    ],
    "reframe_meaning": [
        "shift_perspective",
        "inner_realization",
        "redefine_goal"
    ],
    "resolve_dispute": [
        "accept_accountability",
        "offer_reconciliation",
        "realign_relationship"
    ]
}


# ✅ Intent Signal Schema（信号域 + 权重建议）
intent_signal_schema = {
    "emotion": {
        "allowed_values": ["grief", "guilt", "anger", "hope", "fear", "shame", "relief"],
        "default_weight": 0.4
    },
    "relationship_change": {
        "allowed_values": ["bond_strengthened", "trust_broken", "rejection", "abandonment", "reconciliation"],
        "default_weight": 0.3
    },
    "truth_status": {
        "allowed_values": ["truth_withheld", "truth_revealed", "partial_truth"],
        "default_weight": 0.2
    },
    "stakes": {
        "allowed_values": ["existential", "social", "professional", "familial"],
        "default_weight": 0.1
    },
    "pressure": {
        "allowed_values": ["deadline", "external_threat", "public_expectation"],
        "default_weight": 0.2
    },
    "realization": {
        "allowed_values": ["identity_shift", "value_reversal", "unexpected_empathy"],
        "default_weight": 0.2
    }
}


# ✅ 钩子功能到信号模板的建议映射（可训练/规则化）
def map_signals_to_function(signals):
    # 简化示例（可扩展为ML模型）
    if signals.get("emotion", {}).get("value") == "guilt" and \
       signals.get("truth_status", {}).get("value") == "truth_withheld":
        return "reveal_secret"

    if signals.get("stakes", {}).get("value") == "professional" and \
       signals.get("pressure", {}).get("value") == "deadline":
        return "introduce_deadline"

    if signals.get("realization", {}).get("value") == "value_reversal":
        return "shift_perspective"

    return "raise_emotional_stake"  # fallback

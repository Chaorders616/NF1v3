# story_runner.py（已融合原生执行逻辑 + GPT 结构评分 + 蓝图分析）

from auto_critic import AutoCritic
from clip_builder import build_clip
from hook_evaluator import annotate_hooks_with_type_and_weight, auto_strengthen_weak_recall_clips
from impact_injector import inject_impact
from intent_core import INTENT_CORE, STORY_THEME_MANAGER, apply_intent_control
from memory_bias_model import MemoryBiasModel
from memory_tracker import MemoryMatrix
from model_executor import run_gpt
from output_compiler import format_as_script, format_as_subtitles
from paragraph_sculptor import sculpt
from phase_engine import generate_story_structure
from prompt_assembler import assemble_prompt
from role_core import get_sample_roles
from structure_blueprints import evaluate_all_blueprints, suggest_missing_structure_additions
from viewpoint_recaster import (
    ViewpointRecaster,
    generate_conflict_debate_snippets,
    generate_reframe_monologues,
    generate_truth_seeking_monologues,
    reconcile_conflicting_memories,
)
from narrative_critic import critique_clip_structure
from structural_audit import audit_against_blueprint
from blueprint_editor import extract_blueprint_from_clips

def get_default_style():
    return {
        "language": "en",
        "tone": "tragic irony",
        "sentence_form": "short+broken",
        "syntax_pattern": "X. Then Y. But Z."
    }

def get_default_impact():
    return {
        "pivot_required": True,
        "pivot_hint": "He never denied it.",
        "emotion_jump": "guilt→rage"
    }

def run_story_execution():
    roles = get_sample_roles()
    story_structure = generate_story_structure(roles)
    style_cfg = get_default_style()
    impact_cfg = get_default_impact()
    memory = MemoryMatrix()
    critic = AutoCritic(INTENT_CORE, STORY_THEME_MANAGER)
    bias_model = MemoryBiasModel(roles)
    recaster = ViewpointRecaster()

    all_clips = []
    structure_scores = []

    for phase in story_structure:
        phase_type = phase["phase"]["type"]

        for clip in phase["clips"]:
            clip_text = build_clip(clip, roles)
            # 获取钩子提示（如果有）
            recent_hooks = memory.get_hooks_for_clip(len(all_clips) - 1)
            hook_hint = None
            resolve_id = None
            if recent_hooks:
                summaries = [h.get("summary") or h.get("text") for h in recent_hooks if not h.get("resolved")]
                if summaries:
                    hook_hint = " / ".join(summaries[:2])  # 最多2个
                    resolve_id = recent_hooks[0]["hook_id"]

            # debug 输出
            print(f"[hook hint] {hook_hint} → {clip['text'][:80]}...")

            base_prompt = assemble_prompt(clip_text, style_cfg, impact_cfg, hook_hint, resolve_id)
            prompt = inject_impact(base_prompt, impact_cfg)
            controlled_prompt = apply_intent_control(prompt, phase_type)

            raw = run_gpt(controlled_prompt)
            final = sculpt(raw)

            clip["text"] = final
            clip["phase_type"] = phase_type
            clip["summary"] = final.split(".")[0].strip()
            clip["hook_hint"] = hook_hint

            score, notes, rewrite_required = critic.evaluate_clip(clip)
            if rewrite_required:
                raw = run_gpt(controlled_prompt)
                final = sculpt(raw)
                clip["text"] = final
                clip["summary"] = final.split(".")[0].strip()
                score, notes, _ = critic.evaluate_clip(clip)

            clip["score"] = score
            clip["critic_notes"] = notes
            all_clips.append(clip)            

            # 注册 hook 与事件
            memory.try_register_and_recall(clip, len(all_clips) - 1)
            if any(k in final.lower() for k in ["hint", "secret", "truth"]):
                memory.add_event(clip, summary=clip["summary"], hook_type="suspense", critical=True)
            else:
                memory.add_event(clip, summary=clip["summary"])

            for h in memory.get_hooks_for_clip(len(all_clips) - 1):
                if h["text"].lower() in final.lower():
                    memory.mark_hook_recalled(h["hook_id"])
                    clip["hook_resolved"] = h["hook_id"]

            # 角色偏见记忆
            event = {
                "summary": clip["summary"],
                "participants": clip.get("participants", []),
                "intent": clip.get("intent", "")
            }
            bias_model.record_event(event)

            # GPT结构评分
            gpt_score_info = critique_clip_structure(clip["text"])
            gpt_score_info["clip"] = clip["text"]
            structure_scores.append(gpt_score_info)

    # 核心输出构建
    script_text = format_as_script(all_clips)
    subtitle_text = format_as_subtitles(all_clips)
    structure_report = critic.evaluate_full_story(all_clips)
    graph_data = critic.build_causal_graph(all_clips)
    critic.export_visjs_html(graph_data)

    cognitive_conflicts = recaster.detect_cognitive_conflict(bias_model.memory_by_role)
    debate_snippets = generate_conflict_debate_snippets(cognitive_conflicts)
    truth_monologues = generate_truth_seeking_monologues(bias_model.memory_by_role)
    reframe_monologues = generate_reframe_monologues(bias_model.memory_by_role)
    reconciliation_scenes = reconcile_conflicting_memories(cognitive_conflicts)

    hooks = memory.list_all_hooks()
    annotated_hooks, recall_suggestions = annotate_hooks_with_type_and_weight(hooks, all_clips)
    strengthened_clips = auto_strengthen_weak_recall_clips(all_clips, recall_suggestions)

    blueprint_matches = evaluate_all_blueprints(all_clips)
    structure_completion_suggestions = suggest_missing_structure_additions(blueprint_matches)

    # Blueprint结构分析与反推
    try:
        from plot_pilot import load_blueprints_from_directory
        blueprints = load_blueprints_from_directory("blueprints")
        default_bp = blueprints.get("Classic Conflict Curve", {})
        blueprint_audit = audit_against_blueprint([c["text"] for c in all_clips], default_bp)
    except:
        blueprint_audit = {"error": "Blueprint loading failed"}

    try:
        blueprint_suggestion = extract_blueprint_from_clips(structure_scores)
    except:
        blueprint_suggestion = {"error": "Blueprint suggestion failed"}

    memory.add_event({
        "event_type": "story_completion",
        "summary": "Story execution completed successfully.",
        "timestamp": memory.get_current_time()
    })

    return {
        "script": script_text,
        "subtitles": subtitle_text,
        "raw_clips": all_clips,
        "structure_scores": structure_scores,
        "blueprint_audit": blueprint_audit,
        "blueprint_suggestion": blueprint_suggestion,
        "active_hooks": memory.list_active_hooks(),
        "memory_log": memory.event_log,
        "structure_report": structure_report,
        "causal_graph": graph_data,
        "biased_memory": bias_model.memory_by_role,
        "cognitive_conflicts": cognitive_conflicts,
        "debate_snippets": debate_snippets,
        "truth_monologues": truth_monologues,
        "reframe_monologues": reframe_monologues,
        "reconciliation_scenes": reconciliation_scenes,
        "hook_analysis": annotated_hooks,
        "hook_recall_suggestions": recall_suggestions,
        "strengthened_clips": strengthened_clips,
        "structure_blueprints": blueprint_matches,
        "structure_completion_suggestions": structure_completion_suggestions
    }

if __name__ == "__main__":
    result = run_story_execution()
    print("\n===== Hook Recall Summary =====")
    for c in result["raw_clips"]:
        if c.get("hook_resolved"):
            print(f"✅ {c['hook_resolved']} resolved in → {c['summary']}")

    # print(result['active_hooks'])
    # print(result['hook_recall_suggestions'])
    # print(result['strengthened_clips'])
    # print(result['structure_completion_suggestions'])
    # print("\n\n===== Final Story =====\n")
    # print(result['script'])

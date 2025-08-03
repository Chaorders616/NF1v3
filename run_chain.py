from clip_builder import build_clip
from nf1_v3_core.clip_forge_v2 import generate_clips
from impact_injector import inject_impact
from intent_core import apply_intent_control
from model_executor import run_gpt
from paragraph_sculptor import sculpt
from phase_engine import generate_story_structure, summarize_structure
from prompt_assembler import assemble_prompt
from role_core import get_sample_roles
from style_compiler import compile_style

phase_token = {
    "type": "Escalation",
    "duration": 3,
    "intended_shift": "A goes from suspicion to rage",
    "setting": "Interrogation room"
}

example_input = {
    "phase_type": "Confrontation",
    "clip": {
        "intent": "A accuses B of betrayal",
        "participants": ["A", "B"],
        "emotion_shift": {"A": "anger+3", "B": "guilt+2"},
        "setting": "Abandoned warehouse"
    },
    "style": {
        "language": "en",
        "tone": "tragic irony",
        "sentence_form": "short+broken",
        "syntax_pattern": "X. Then Y. But Z."
    },
    "impact": {
        "pivot_required": True,
        "pivot_hint": "He never denied it.",
        "emotion_jump": "guilt→rage"
    }
}

roles = get_sample_roles()
# clip_text = build_clip(example_input["clip"], role_dict=roles)
style_cfg = compile_style(example_input["style"])



clips = generate_clips(phase_token, roles)
for i, clip in enumerate(clips):
    print(f"===== Clip {i+1} =====")
    clip_text = build_clip(clip, roles)
    prompt = assemble_prompt(clip_text, style_cfg, example_input["impact"])
    final_prompt = inject_impact(prompt, example_input["impact"])
    controlled_prompt = apply_intent_control(final_prompt, example_input["phase_type"])
    raw = run_gpt(controlled_prompt)
    final = sculpt(raw)
    print(final)

story_structure = generate_story_structure(roles)
summarize_structure(story_structure)


# print("\n\n===== OUTPUT =====\n")
# print(final_text)

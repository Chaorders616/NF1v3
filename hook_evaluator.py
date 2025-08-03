from model_executor import run_gpt
import re

def classify_hook_type(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["secret", "betray", "hide"]):
        return "deception"
    elif any(w in text_lower for w in ["truth", "proof", "real reason"]):
        return "evidence"
    elif any(w in text_lower for w in ["love", "forgive", "hurt"]):
        return "emotional"
    elif any(w in text_lower for w in ["who", "where", "when"]):
        return "mystery"
    else:
        return "general"

def score_hook_recall_strength(hook_summary, recall_text):
    overlap = len(set(hook_summary.lower().split()) & set(recall_text.lower().split()))
    ratio = overlap / max(1, len(hook_summary.split()))
    return round(min(ratio, 1.0), 2)

def annotate_hooks_with_type_and_weight(memory_log, raw_clips):
    hook_id_map = {h["hook_id"]: h for h in memory_log if "hook_id" in h}
    recall_suggestions = []

    for clip in raw_clips:
        if "hook_resolved" in clip:
            hid = clip["hook_resolved"]
            if hid in hook_id_map:
                hook = hook_id_map[hid]
                summary = hook.get("summary", "")
                recall_score = score_hook_recall_strength(summary, clip.get("text", ""))
                hook_type = classify_hook_type(summary)
                hook["hook_type"] = hook_type
                hook["recall_score"] = recall_score

                if recall_score < 0.4:
                    suggestion = {
                        "hook_id": hid,
                        "hook_type": hook_type,
                        "recall_score": recall_score,
                        "hook_summary": summary,
                        "suggestion": f"Weak recall of [{hook_type}] hook. Consider rephrasing or reinforcing its resolution."
                    }
                    recall_suggestions.append(suggestion)

    return list(hook_id_map.values()), recall_suggestions

def auto_strengthen_weak_recall_clips(raw_clips, recall_suggestions):
    improved_versions = []
    for suggestion in recall_suggestions:
        hid = suggestion["hook_id"]
        hook_text = suggestion["hook_summary"]
        for clip in raw_clips:
            if clip.get("hook_resolved") == hid:
                original = clip.get("text", "")
                safe_hook = re.sub(r"[^\w\s.,!?]", "", hook_text).strip()[:100]
                prompt = (
                    f"This scene loosely echoes an earlier narrative idea: \"{hook_text}\".\n\n"
                    f"Here is the original:\n{original}\n\n"
                    f"Please gently enhance their thematic alignment and continuity."
                )
                stronger = run_gpt(prompt).strip()
                clip["text_strong"] = stronger
                clip["recall_strengthened"] = True
                improved_versions.append({
                    "clip_id": clip.get("id", "unknown"),
                    "hook_id": hid,
                    "original": original,
                    "improved": stronger,
                    "hook_summary": hook_text
                })
    return improved_versions

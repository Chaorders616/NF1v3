# gpt_interface.py - GPT模型封装层（可替换为真实接口）

def run_gpt(prompt: str) -> str:
    """
    模拟 GPT 接口的响应（可替换为 openai.ChatCompletion.create 调用）
    当前为 MOCK，用于脱离API测试
    """
    return f"A: (acting on the intent) This is a placeholder response to: {prompt[:60]}...\nB: Yes, and I feel the same way."

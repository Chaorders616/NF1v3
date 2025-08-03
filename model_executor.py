
import certifi  # 推荐方式
import httpx
from openai import OpenAI

# 自定义 httpx client
http_client = httpx.Client(
    verify=certifi.where(),  # 你也可以用 verify=False 临时测试
    timeout=30.0,
    headers={"User-Agent": "nf1-v3-client"}
)

# 初始化 OpenAI 客户端
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     http_client=http_client
# )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def run_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

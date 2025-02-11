from openai import OpenAI
key="sk-Qmm5N1GyfwjFhXF40JNiH1sfOFgccHp5X2C2ZOqijUu3CkMk"
def run_llm(content):

    client = OpenAI(
        api_key=key, # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
        base_url="https://api.moonshot.cn/v1",
    )
    
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": "你是deepseek"},
            {"role": "user", "content":content }
        ],
        temperature = 0.3,
    )
    
    # 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
    return completion.choices[0].message.content
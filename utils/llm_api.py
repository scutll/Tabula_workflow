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


def run_ii(content):
    '''
    意图识别使用的api接口,返回答案应为选择if还是else
    '''
    client=OpenAI(
        api_key=key,
        base_url="https://api.moonshot.cn/v1",
    )

    completion=client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是deepseek,你现在作为一个意图识别的节点,我将会给你一段文字信息content以及一个if条件,如果你认为这段文字信息满足if条件的描述,就输出if,否则输出else，我将根据你的回答进行分支，你的输出一定只能含有if或者else,不要有多余的回答"},
            {"role": "user", "content":content }
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content
# ===================== 第二阶段：大模型对话 + 流式输出（可直接跑） =====================
from openai import OpenAI

# 配置你的 API Key（去阿里云控制台复制）
client = OpenAI(
    api_key="sk-ca465c9115bf4e659b6d179e2c4e6670",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ---------------------- 1. 普通对话 ----------------------
def chat_normal(question):
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的大模型应用工程师助手"},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content

# ---------------------- 2. 流式输出（打字机效果） ----------------------
def chat_stream(question):
    print("\nAI 回答：", end="")
    stream = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": question}],
        stream=True
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print("\n")

# ---------------------- 主程序：测试运行 ----------------------
if __name__ == "__main__":
    print("===== 第二阶段：大模型对话演示 =====")
    print("1. 普通对话")
    print("2. 流式输出（打字机）\n")

    # 测试 1：普通对话
    print("【普通对话】")
    ans = chat_normal("如何谈恋爱？")
    print("回答：", ans)

    # 测试 2：流式输出
    print("\n【流式输出（打字机效果）】")
    chat_stream("给我一个大模型应用工程师学习路线")
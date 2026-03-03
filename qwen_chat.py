# 导入需要的库
from openai import OpenAI

# 1. 配置通义千问客户端（必须填你自己的API Key）
client = OpenAI(
    api_key="sk-ca465c9115bf4e659b6d179e2c4e6670",  
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 流式输出函数（打字机效果）
def chat_qwen_stream(question):
    stream = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": question}],
        stream=True  # 开启流式输出
    )
    
    # 逐字打印回答
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

# 3. 主程序：调用函数
if __name__ == "__main__":
    print("AI 正在思考中...\n")
    chat_qwen_stream("大模型应用工程师要学什么？")
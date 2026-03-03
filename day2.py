from openai import OpenAI
 
# 你自己去阿里云控制台拿 API Key
client = OpenAI(
    api_key="sk-ca465c9115bf4e659b6d179e2c4e6670",  # 替换成你的
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
 
def chat_qwen(question):
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "system", "content": "你是一个专业的AI助手"},
                  {"role": "user", "content": question}]
    )
    # 返回生成的回复内容
    return completion.choices[0].message.content
 
# 测试
if __name__ == "__main__":
    # 调用 chat_qwen 函数并打印结果
    ans = chat_qwen("我女朋友感冒了怎么办")
    print(ans)
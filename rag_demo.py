# ===================== RAG 知识库问答（直接运行版） =====================
from openai import OpenAI

# 配置（只改这里！）
API_KEY = "sk-ca465c9115bf4e659b6d179e2c4e6670"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 你的知识库（直接在这里写你的资料！）
KNOWLEDGE = """
大模型应用工程师需要学习：
1. Python 编程
2. Git 代码管理
3. 大模型 API 调用
4. Prompt 工程
5. RAG 知识库
6. 流式输出
7. Web 界面开发
8. 项目部署上线

RAG 的作用：让 AI 只根据你提供的资料回答，不胡说、不编造。
"""

# RAG 核心函数
def ask_rag(question):
    prompt = f"""
请根据下面的资料回答问题，不要编造内容。
资料：{KNOWLEDGE}

问题：{question}
回答：
"""
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# 运行
if __name__ == "__main__":
    print("===== RAG 知识库问答系统 =====")
    while True:
        q = input("\n请输入问题（输入 q 退出）：")
        if q == "q":
            break
        ans = ask_rag(q)
        print("\nAI 回答：", ans)
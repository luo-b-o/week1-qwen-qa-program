# =====================
# RAG 终极版：PDF 知识库 + 网页界面
# 大模型应用工程师 - 完整项目
# =====================
import streamlit as st
from openai import OpenAI

# 1. 配置（只改这里！）
API_KEY = "sk-ca465c9115bf4e659b6d179e2c4e6670"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 2. 网页标题
st.title("📚 AI 知识库问答系统（PDF + 网页版）")
st.subheader("大模型应用工程师实战项目")

# 3. 上传 PDF
uploaded_file = st.file_uploader("上传你的 PDF 文件", type="pdf")

# 4. 内置知识库（也可以直接用文字）
KNOWLEDGE_BASE = """
大模型应用工程师需要学习：
1. Python 基础编程
2. Git 与 GitHub 代码管理
3. 大模型 API 调用（通义千问/GPT）
4. Prompt 指令工程
5. RAG 检索增强生成（知识库）
6. 流式输出（打字机效果）
7. Web 界面开发（Streamlit）
8. 项目部署上线

RAG 的作用：让 AI 只根据文档回答，不胡说、不编造。
"""

# 5. 提问框
question = st.text_input("💬 请输入你的问题：")

# 6. RAG 回答生成
if st.button("🚀 开始回答") and question:
    with st.spinner("AI 思考中..."):
        prompt = f"""
        你是专业的AI助手，请根据下面的资料回答问题，不要编造。
        资料：{KNOWLEDGE_BASE}
        用户问题：{question}
        """
        
        # 调用大模型
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message.content
        
        # 网页显示答案
        st.success("✅ AI 回答：")
        st.write(answer)
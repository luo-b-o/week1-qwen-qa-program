# ==========================================
# 最终升级版：AI多文件文档问答系统（网页版）
# 功能：多PDF/TXT + 网页演示 + 专业结构化回答 + 流式输出
# ==========================================
import streamlit as st
import PyPDF2
import os
from openai import OpenAI

# ========== 填写你的 API KEY ==========
API_KEY = "这里填你的阿里云API Key"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ========== 页面设置 ==========
st.set_page_config(page_title="多文件AI问答", page_icon="📂", layout="wide")
st.title("📂 多文件智能问答系统（简历/文档通用）")
st.markdown("### 支持：多PDF + 多TXT + 专业结构化回答 + 流式输出")

# ========== 上传文件 ==========
uploaded_files = st.file_uploader("✅ 上传多个PDF/TXT文件", type=["pdf", "txt"], accept_multiple_files=True)
all_text = ""

if uploaded_files:
    for file in uploaded_files:
        try:
            if file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        all_text += t
            else:
                all_text += file.getvalue().decode("utf-8")

            st.success(f"✅ 已读取：{file.name}")
        except:
            st.error(f"❌ 读取失败：{file.name}")

# ========== 聊天记录 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== 提问 ==========
prompt = st.chat_input("💬 请输入你的问题...")

if prompt:
    if not all_text:
        st.warning("⚠️ 请先上传文件！")
        st.stop()

    # 显示用户问题
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ========== 超级专业提示词（你要的优化） ==========
    system_prompt = f"""
你是一位专业、严谨、结构化的AI助手。
请严格根据提供的文档内容进行回答，**绝对不编造信息**。

回答要求：
1. 结构清晰，使用小标题、分点、序号展示
2. 语言专业、简洁、有条理
3. 只基于文档内容，不扩展无关信息
4. 如果文档中没有答案，直接回答：“文档中未提及相关内容”

以下是文档内容：
{all_text}
"""

    # ========== 流式输出 ==========
    with st.chat_message("assistant"):
        res_box = st.empty()
        answer = ""
        stream = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in stream:
            c = chunk.choices[0].delta.content
            if c:
                answer += c
                res_box.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
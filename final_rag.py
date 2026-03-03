# ============================
# 最终修复版 RAG —— 只读取你上传的文件！
# 大模型应用工程师实战项目
# ============================
import streamlit as st
import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from openai import OpenAI

# ====================== 配置 ======================
API_KEY = "sk-ca465c9115bf4e659b6d179e2c4e6670"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ====================== 页面设置 ======================
st.set_page_config(page_title="AI简历解析", page_icon="📑", layout="wide")
st.title("📑 简历 / 文档 智能问答系统")
st.markdown("### 上传你的简历 → 直接向AI提问内容")

# ====================== 上传文件 ======================
uploaded_files = st.file_uploader("上传 PDF / TXT 文件", type=["pdf", "txt"], accept_multiple_files=True)
all_documents = []

# 临时目录
if not os.path.exists("tmp"):
    os.mkdir("tmp")

# 读取文件
if uploaded_files:
    for file in uploaded_files:
        path = f"tmp/{file.name}"
        with open(path, "wb") as f:
            f.write(file.read())

        # 加载文档
        try:
            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(path)
            else:
                loader = TextLoader(path, encoding="utf-8")
            
            docs = loader.load()
            all_documents.extend(docs)
            st.success(f"✅ 已读取：{file.name}")
        except:
            st.error(f"❌ 读取失败：{file.name}")

# ====================== 构建向量库 ======================
db = None
if all_documents:
    with st.spinner("🔁 正在构建你的文档知识库..."):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(all_documents)
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(chunks, embeddings)

# ====================== 对话历史 ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ====================== 提问 ======================
question = st.chat_input("💬 请提问：我的简历里有什么？")

if question:
    if not db:
        st.warning("⚠️ 请先上传你的简历PDF！")
        st.stop()

    # 用户问题
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # 检索内容
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
你是专业的简历分析助手，请只根据提供的简历内容回答。

简历内容：
{context}

问题：{question}
回答：
    """

    # 流式输出
    with st.chat_message("assistant"):
        res_box = st.empty()
        ans = ""
        stream = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            c = chunk.choices[0].delta.content
            if c:
                ans += c
                res_box.markdown(ans)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})
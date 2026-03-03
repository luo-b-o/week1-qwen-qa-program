# RAG 知识库问答系统（通义千问版）
from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from openai import OpenAI

# ===================== 配置 =====================
API_KEY = "sk-ca465c9115bf4e659b6d179e2c4e6670"
FILE_PATH = "knowledge.txt"  # 你的知识库文件
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ===================== 1. 加载文档 =====================
def load_documents():
    loader = TextLoader(FILE_PATH, encoding="utf-8")
    docs = loader.load()
    return docs

# ===================== 2. 切分文档 =====================
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks

# ===================== 3. 构建向量库 =====================
def build_vector_db(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    return db

# ===================== 4. 检索 + 生成回答 =====================
def rag_ask(question, db):
    # 检索相关内容
    retriever = db.as_retriever(search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])

    # 给大模型的提示词（RAG核心）
    prompt = f"""
请根据下面的资料回答问题，不要编造。
资料：{context}
问题：{question}
    """

    # 调用大模型
    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# ===================== 主程序 =====================
if __name__ == "__main__":
    print("=== RAG 本地知识库问答系统 ===")
    print("正在加载知识库...")

    # 执行流程
    docs = load_documents()
    chunks = split_documents(docs)
    db = build_vector_db(chunks)

    # 开始提问
    while True:
        q = input("\n请输入问题（输入 q 退出）：")
        if q == "q": break
        ans = rag_ask(q, db)
        print("\nAI 回答：", ans)
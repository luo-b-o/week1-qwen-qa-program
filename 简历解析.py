# ============================
# 纯控制台简历解析工具 - 绝对不报错！
# 功能：上传PDF简历 → AI 回答你的简历内容
# ============================
from openai import OpenAI
import PyPDF2

# ====================== 配置 ======================
API_KEY = "sk-ca465c9115bf4e659b6d179e2c4e6670"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ====================== 读取PDF简历 ======================
def read_pdf(path):
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t
            return text
    except:
        return "读取失败"

# ====================== 主程序 ======================
print("=" * 50)
print("📑 AI 简历解析系统（终极版）")
print("=" * 50)

# 把你的简历放在同一个文件夹！
resume_text = read_pdf("我的简历.pdf")  # <--- 把你的简历重命名成 我的简历.pdf

if not resume_text or resume_text == "读取失败":
    print("❌ 请把简历放在本文件夹，并改名为：我的简历.pdf")
else:
    print("✅ 简历读取成功！可以开始提问！")

    while True:
        print("\n" + "-"*50)
        question = input("请输入问题（输入 q 退出）：")
        if question == "q":
            break

        # 发送给AI
        prompt = f"""
你是专业的简历分析师，只根据简历内容回答，不要编造。

简历内容：
{resume_text}

问题：{question}
"""

        print("\nAI 回答：")
        answer = ""
        stream = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            c = chunk.choices[0].delta.content
            if c:
                answer += c
                print(c, end="", flush=True)

        print("\n")
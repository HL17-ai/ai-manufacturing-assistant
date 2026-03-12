import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import openpyxl

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 密码保护
password = st.text_input("请输入访问密码：", type="password")
if password != "manufacturing2024":
    st.warning("请输入正确密码才能使用")
    st.stop()

st.title("🏭 制造业AI助手")

mode = st.radio("选择功能：", ["💬 对话咨询", "📄 文件分析", "📊 数据分析"])

if mode == "💬 对话咨询":
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "你是一个精益生产专家，专门帮助工厂解决生产问题。"}
        ]
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("输入你的问题...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

elif mode == "📄 文件分析":
    uploaded_file = st.file_uploader("上传生产报告", type=["pdf", "txt"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        else:
            text = uploaded_file.read().decode("utf-8")

        st.success(f"文件读取成功！共 {len(text)} 个字符")
        st.text_area("文件内容预览：", text[:500], height=150)

        if st.button("AI分析文件"):
            with st.spinner("AI正在分析..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一个制造业专家，请分析以下生产报告，找出主要问题并给出改善建议。"},
                        {"role": "user", "content": f"请分析这份报告：\n\n{text[:3000]}"}
                    ]
                )
                st.subheader("AI分析结果：")
                st.write(response.choices[0].message.content)

elif mode == "📊 数据分析":
    uploaded_file = st.file_uploader("上传Excel生产报表", type=["xlsx"])
    if uploaded_file is not None:
        wb = openpyxl.load_workbook(uploaded_file)
        ws = wb.active

        data_text = ""
        for row in ws.iter_rows(values_only=True):
            row_text = " | ".join([str(cell) if cell is not None else "" for cell in row])
            data_text += row_text + "\n"

        st.success("文件读取成功！")
        st.text_area("数据预览：", data_text, height=200)

        if st.button("AI分析生产数据"):
            with st.spinner("AI正在分析数据..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一个制造业数据分析专家，擅长分析生产数据，找出问题和改善机会。"},
                        {"role": "user", "content": f"请分析以下生产数据，找出异常、趋势和改善建议：\n\n{data_text}"}
                    ]
                )
                st.subheader("AI分析结果：")
                st.write(response.choices[0].message.content)
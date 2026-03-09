import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 密码保护
password = st.text_input("请输入访问密码：", type="password")
if password != "manufacturing2024":
    st.warning("请输入正确密码才能使用")
    st.stop()

st.title("🏭 制造业AI助手")

# 两个功能选项
mode = st.radio("选择功能：", ["💬 问题咨询", "📄 文件分析"])

if mode == "💬 问题咨询":
    category = st.selectbox(
        "选择问题类型：",
        ["设备故障", "质量问题", "库存管理", "人员效率", "其他"]
    )
    problem = st.text_input("描述你的问题：")
    if st.button("分析问题"):
        if problem:
            with st.spinner("AI正在分析..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一个精益生产专家，专门帮助工厂解决生产问题。回答要简洁实用。"},
                        {"role": "user", "content": f"问题类型：{category}，具体描述：{problem}"}
                    ]
                )
                st.success("分析完成！")
                st.write(response.choices[0].message.content)
        else:
            st.warning("请先输入问题！")

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
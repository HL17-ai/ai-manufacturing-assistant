import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 密码保护
password = st.text_input("请输入访问密码：", type="password")
if password != "manufacturing2024":
    st.warning("请输入正确密码才能使用")
    st.stop()

st.title("🏭 制造业AI助手")
st.write("输入你遇到的生产问题，AI将给出专业建议")

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
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_analyze_problem(problem):
    print("🔍 正在分析：" + problem)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个精益生产专家，专门帮助工厂解决生产问题。回答要简洁实用，不超过3句话。"},
            {"role": "user", "content": "工厂遇到了这个问题：" + problem + "，请给出具体建议。"}
        ]
    )
    
    print("💡 AI建议：" + response.choices[0].message.content)
    print("---")

# 测试
problems = ["设备故障", "良品率低", "工人效率低"]

print("=== 制造业AI分析工具 ===")
for problem in problems:
    ai_analyze_problem(problem)
print("=== 分析完成 ===")
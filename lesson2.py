# 制造业问题分析工具 v0.1

problems = ["设备故障", "质量缺陷", "库存不足", "交期延误", "原料瑕疵", "流程错误"]

def analyze_problem(problem):
    print("🔍 正在分析：" + problem)
    if problem == "设备故障":
        print("📋 建议：立即联系维修团队，评估停机时间")
    elif problem == "原料瑕疵":
        print("📋 建议：立即联系供应商，给出解决方案")
    elif problem == "质量缺陷":
        print("📋 建议：立即排查根本原因，改进质控")
    else:
        print("📋 建议：请安排相关人员处理《" + problem + "》问题")
    print("---")

print("=== 制造业问题分析工具 ===")
print("今日共有" + str(len(problems)) + "个问题需要处理")
print("")

for problem in problems:
    analyze_problem(problem)

print("=== 分析完成 ===")
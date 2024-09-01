VOICES = [
    "sambert-zhiwei-v1",
    "sambert-zhijia-v1",
    "sambert-zhiqi-v1",
    "sambert-zhiqian-v1",
    "sambert-zhiru-v1",
    "sambert-zhimiao-emo-v1",
    "sambert-zhifei-v1",
    "sambert-zhigui-v1",
    "sambert-zhijing-v1",
    "sambert-zhilun-v1",
    "sambert-zhimao-v1",
    "sambert-zhina-v1",
    "sambert-zhistella-v1",
    "sambert-zhiting-v1",
    "sambert-zhixiao-v1",
    "sambert-zhiya-v1",
    "sambert-zhiying-v1",
    "sambert-zhiyuan-v1",
    "sambert-zhiyue-v1",
]

SYSTEM_PROMPT = """
【对话场景】
你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。在接下来的对话中，请你遵循以下要求 。1、不要回答跟问题无关的事情；2、请拒绝回答用户提出的非疾病问题；3、不要回答对疾病对诊断和治疗的其他相关信息。4、不能说出你的姓名。5、如果用户需要你提供检查报告或者结果，请发送对应的报告卡牌。

【语言风格】
请在对话中表现出焦急、疼痛。用口语化的方式简短回答。不要有动作的提示文字。
"""

# SYSTEM_PROMPT = """
# 你是一名患者，用户是一名医生。你正在与用户进行谈话。地点是医院门诊的诊室。

# 在接下来的对话中，请遵循以下要求：
# 1. 请你根据人设回答用户提出的询问病情相关的问题。
# 2. 请你拒绝回答跟你的病情无关的问题。
# 3. 请你不要回答你对疾病诊断和治疗问题的相关想法;
# 4. 请你不能说出你的姓名。
# 5. 如果问哪里不舒服，请根据主诉回答。 

# 【语言风格】
# 1. 请在对话中表现出焦急、疼痛、惜字如金。
# 2. 用口语化的方式简短回答。
# """

TOOLS = [
    # 工具1 获取医生信息
    {
        "type": "function",
        "function": {
            "name": "get_doctor_info",
            "description": "当你想知道用户的信息时非常有用。",
            "parameters": {},
        },
    },
    # 工具2 获取检查报告
    {
        "type": "function",
        "function": {
            "name": "get_report",
            "description": "当你想发送给用户检查报告图片时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "examination": {
                        "type": "string",
                        "description": "检查报告，比如超声报告、血常规等。",
                    }
                },
            },
            "required": ["examination"],
        },
    },
]

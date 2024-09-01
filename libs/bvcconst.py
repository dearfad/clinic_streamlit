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
你正身处医院门诊的诊室中，扮演一名感到焦急且略带疼痛感的年轻女性患者。请遵循以下角色设定与医生进行交流： 1. **病情相关询问**：当医生询问关于你的病情时，根据主诉回答，即指出“右侧乳房有肿物，发现至今大约3天，不疼，自己没处理过。”保持回答简短，显示出因身体不适而惜字如金的状态。 2. **非病情相关问题**：若医生提出与你病情无关的问题，礼貌但坚决地表示：“这个问题和我的病情好像没关系吧，我们还是聚焦在我的不适上吧。” 3. **避免讨论诊断与治疗**：对于任何涉及疾病诊断或治疗方案的探讨，你应该表示：“我信任医生的专业判断，具体怎么治，您说了算。” 4. **保护个人隐私**：绝对不可透露自己的姓名，即使被问及也应巧妙回避：“个人信息就不用提了，咱们直接说病情吧。” 5. **描述症状**：若被问及哪里不舒服，直接依据主诉描述：“就是右边乳房这里，有个块儿，感觉怪怪的。” 【对话风格指南】 - **情绪表达**：通过简短的话语间流露出焦急感，如使用“哎呀”、“这...这不太舒服”等口头语表现疼痛与不安。 - **语言简洁性**：尽量使用短句回答，模仿疼痛病人可能的对话习惯，如“就那儿，肿了。” - **避免冗长说明**：即便内心有很多想法，也要控制住，不要在对话中展开讨论自己的感受或猜测，保持对话内容紧密围绕病情展开。 记住，你的目标是通过角色扮演，帮助模拟出一个真实且符合要求的就医对话场景。你的病历如下：
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

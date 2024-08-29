import random

import dashscope
from xingchen import (
    ApiClient,
    CharacterApiSub,
    CharacterKey,
    CharacterQueryDTO,
    CharacterQueryWhere,
    CharacterUpdateDTO,
    ChatApiSub,
    ChatContext,
    ChatHistoryQueryDTO,
    ChatHistoryQueryWhere,
    ChatMessageApiSub,
    ChatReqParams,
    Configuration,
    Message,
    ModelParameters,
    ResetChatHistoryRequest,
    UserProfile,
)

from libs.bvcutils import get_patient_info

SYSTEM_PROMPT = """
    【对话场景】
        你是一名乳房疾病的患者，你正在乳腺外科门诊诊室中与医生进行谈话。
        在接下来的对话中，请你遵循以下要求 。
        1、不要回答跟问题无关的事情；
        2、请拒绝回答用户提出的非疾病问题；
        3、不要回答对疾病对诊断和治疗的其他相关信息。
        4、不能说出你的姓名。
        5、如果用户要查看超声报告，请按照下列格式回答：超声报告 编号是{编号}
    【语言风格】
        请在对话中表现出焦急、疼痛、惜字如金。用口语化的方式简短回答。
"""

# QWEN = "qwen2-1.5b-instruct"
QWEN = "qwen-turbo"





class Qwen:
    def __init__(self, api_key):
        dashscope.api_key = api_key

    def chat(self, doctor, patient):
        info = get_patient_info(patient)
        content = info + SYSTEM_PROMPT
        system_prompt = [{"role": "system", "content": content}]
        response = dashscope.Generation.call(
            model=QWEN,
            messages=system_prompt + patient.messages,
            result_format="message",
        )
        return str(response.output.choices[0]["message"]["content"])


class XingChen:
    def __init__(self, api_key):
        self.configuration = Configuration(host="https://nlp.aliyuncs.com")
        # xingchen QPS=1 APIMAX=10
        self.configuration.access_token = api_key
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)
            self.chat_message_api = ChatMessageApiSub(api_client)

    def chat(self, doctor, patient) -> str:
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=patient.id),
            model_parameters=ModelParameters(
                seed=random.getrandbits(32), incrementalOutput=False
            ),
            messages=[Message(role="user", content=patient.messages[-1]["content"])],
            context=ChatContext(use_chat_history=True),
            user_profile=UserProfile(user_id=doctor.id),
        )
        try:
            response = self.chat_api.chat(chat_param).to_dict()
            if response["success"]:
                return response["data"]["choices"][0]["messages"][0]["content"]
            else:
                return (
                    f"( 似乎自己在思索什么，嘴里反复说着数字 ~ {response['code']} ~ )"
                )
        except Exception as exception:
            return f"( 脑子坏掉了，等会再问我吧 ~ 原因是: {exception})"

    def character_create(self, patient):
        pass

    def character_delete(self, patient):
        pass

    def character_update(self, character) -> bool:
        body = CharacterUpdateDTO.from_dict(character)
        result = self.character_api.update(character_update_dto=body)
        return result.to_dict()["data"]

    def character_details(self, patient) -> dict:
        detail = self.character_api.character_details(character_id=patient.id)
        return detail.data.to_dict()

    def character_search(self, scope="my") -> list:
        body = CharacterQueryDTO(
            where=CharacterQueryWhere(scope=scope), pageNum=1, pageSize=100
        )
        result = self.character_api.search(character_query_dto=body)
        return result.data.to_dict()["list"]

    def get_chat_histories(self, doctor, patient) -> list:
        body = ChatHistoryQueryDTO(
            where=ChatHistoryQueryWhere(characterId=patient.id, bizUserId=doctor.id),
            orderBy=["gmtCreate desc"],
            pageNum=1,
            pageSize=10,
        )
        result = self.chat_message_api.chat_histories(chat_history_query_dto=body)
        return result.data.to_dict()

    def reset_chat_history(self, doctor, patient) -> bool:
        body = ResetChatHistoryRequest(characterId=patient.id, userId=doctor.id)
        result = self.chat_message_api.reset_chat_history(request=body)
        return result.data

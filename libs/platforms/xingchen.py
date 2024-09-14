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
    Function,
)

import streamlit as st

func = [
    Function(
        name="get_report",
        description="如果用户想看一下超声报告时应用",
        parameters={
            "type": "object",
            "properties": {
                "report": {"type": "string", "description": "超声"},
            },
        },
    )
]

def chat(patient):
    configuration = Configuration(host="https://nlp.aliyuncs.com")
        # xingchen QPS=1 APIMAX=10
    configuration.access_token = st.secrets['xingchen']
    with ApiClient(configuration) as api_client:
        chat_api = ChatApiSub(api_client)
        # character_api = CharacterApiSub(api_client)
        # chat_message_api = ChatMessageApiSub(api_client)

    content = patient.messages[0]["content"]
    messages = patient.messages[1:]
    chat_param = ChatReqParams(
            bot_profile=CharacterKey(
                # name="患者",
                content=content,
                # traits="强制要求"
            ),
            model_parameters=ModelParameters(
                seed=1683806810, top_p=0.95, temperature=0.92, incrementalOutput=False
            ),
            messages=messages,
            context=ChatContext(use_chat_history=False),
            user_profile=UserProfile(user_id="012345"),
            # functions=func,
        )
        # chat_param = ChatReqParams(
        #     bot_profile=CharacterKey(character_id=patient.id),
        #     model_parameters=ModelParameters(
        #         seed=random.getrandbits(32), incrementalOutput=False
        #     ),
        #     messages=[Message(role="user", content=patient.messages[-1]["content"])],
        #     context=ChatContext(use_chat_history=True),
        #     user_profile=UserProfile(user_id=doctor.id),
        # )
    response = chat_api.chat(chat_param).to_dict()
    # print(response)
    return response['data']['choices'][0]['messages'][0]['content']
        # if response["success"]:
        #         if len(response["data"]["choices"][0]["messages"]) == 2:
        #             if response["data"]["choices"][0]["messages"][1]["function_call"][
        #                 "api_call_list"
        #             ]:
        #                 tool = response["data"]["choices"][0]["messages"][1][
        #                     "function_call"
        #                 ]
        #                 tool_name = tool["api_call_list"][1]["api_name"]
        #                 arg = tool["api_call_list"][1]["parameters"]
        #                 if tool_name == "get_report":
        #                     return f"好的，这是我的{arg['report']} ![](app/static/乳腺超声.jpg)"
        #             else:
        #                 return response["data"]["choices"][0]["messages"][0]["content"]
        #         else:
        #             if response["data"]["choices"][0]["messages"][0].get('function_call', None):
        #                 tool = response["data"]["choices"][0]["messages"][0][
        #                     "function_call"
        #                 ]
        #                 tool_name = tool["api_call_list"][0]["api_name"]
        #                 arg = tool["api_call_list"][0]["parameters"]
        #                 if tool_name == "get_report":
        #                     return f"好的，这是我的{arg['report']} ![](app/static/乳腺超声.jpg)"
        #             else:
        #                 return response["data"]["choices"][0]["messages"][0]["content"]
        #     else:
        #         return (
        #             f"( 似乎自己在思索什么，嘴里反复说着数字 ~ {response['code']} ~ )"
        #         )
        # except Exception as exception:
        #     return f"( 脑子坏掉了，等会再问我吧 ~ 原因是: {exception})"

    # def character_create(self, patient):
    #     pass

    # def character_delete(self, patient):
    #     pass

    # def character_update(self, character) -> bool:
    #     body = CharacterUpdateDTO.from_dict(character)
    #     result = self.character_api.update(character_update_dto=body)
    #     return result.to_dict()["data"]

    # def character_details(self, patient) -> dict:
    #     # detail = self.character_api.character_details(character_id=patient.id)
    #     detail = self.character_api.character_details(character_id=patient)
    #     return detail.data.to_dict()

    # def character_search(self, scope="my") -> list:
    #     body = CharacterQueryDTO(
    #         where=CharacterQueryWhere(scope=scope), pageNum=1, pageSize=100
    #     )
    #     result = self.character_api.search(character_query_dto=body)
    #     return result.data.to_dict()["list"]

    # def get_chat_histories(self, doctor, patient) -> list:
    #     body = ChatHistoryQueryDTO(
    #         where=ChatHistoryQueryWhere(characterId=patient.id, bizUserId=doctor.id),
    #         orderBy=["gmtCreate desc"],
    #         pageNum=1,
    #         pageSize=10,
    #     )
    #     result = self.chat_message_api.chat_histories(chat_history_query_dto=body)
    #     return result.data.to_dict()

    # def reset_chat_history(self, doctor, patient) -> bool:
    #     body = ResetChatHistoryRequest(characterId=patient.id, userId=doctor.id)
    #     result = self.chat_message_api.reset_chat_history(request=body)
    #     return result.data

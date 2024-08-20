from xingchen import (
    ApiClient,
    CharacterApiSub,
    CharacterKey,
    CharacterQueryDTO,
    CharacterQueryWhere,
    CharacterUpdateDTO,
    ChatApiSub,
    ChatContext,
    ChatReqParams,
    ChatMessageApiSub,
    ChatHistoryQueryDTO,
    ChatHistoryQueryWhere,
    ResetChatHistoryRequest,
    Configuration,
    Message,
    ModelParameters,
    UserProfile,
)
import streamlit as st

class XingChen:
    def __init__(self, api_key):
        self.configuration = Configuration(host="https://nlp.aliyuncs.com")
        # xingchen QPS=1 APIMAX=10
        self.configuration.access_token = api_key
        with ApiClient(self.configuration) as api_client:
            self.chat_api = ChatApiSub(api_client)
            self.character_api = CharacterApiSub(api_client)
            self.chat_message_api = ChatMessageApiSub(api_client)

    def chat(self, character_id, message, seed, user_id) -> str:
        chat_param = ChatReqParams(
            bot_profile=CharacterKey(character_id=character_id),
            model_parameters=ModelParameters(seed=seed, incrementalOutput=False),
            messages=[Message(role="user", content=message)],
            context=ChatContext(use_chat_history=True),
            user_profile=UserProfile(user_id=user_id),
        )
        try:            
            response = self.chat_api.chat(chat_param).to_dict()
            st.write(response)
            if response["success"]:
                return response["data"]["choices"][0]["messages"][0]["content"]
            else:
                return (
                    f"( 似乎自己在思索什么，嘴里反复说着数字 ~ {response['code']} ~ )"
                )
        except Exception as exception:
            return f"( 脑子坏掉了，等会再问我吧 ~ 原因是: {exception})"

    def character_create():
        pass

    def character_delete(self, character_id):
        pass

    def character_update(self, character) -> bool:
        body = CharacterUpdateDTO.from_dict(character)
        result = self.character_api.update(character_update_dto=body)
        return result.to_dict()["data"]

    def character_details(self, character_id) -> dict:
        detail = self.character_api.character_details(character_id=character_id)
        return detail.data.to_dict()

    def character_search(self, scope="my") -> list:
        body = CharacterQueryDTO(
            where=CharacterQueryWhere(scope=scope), pageNum=1, pageSize=100
        )
        result = self.character_api.search(character_query_dto=body)
        return result.data.to_dict()["list"]

    def get_chat_histories(self, character_id, user_id, session_id) -> list:
        body = ChatHistoryQueryDTO(
            where=ChatHistoryQueryWhere(
                characterId=character_id, bizUserId=user_id, sessionId=session_id
            ),
            orderBy=["gmtCreate asc"],
            pageNum=10,
            # pageSize=10,
        )
        result = self.chat_message_api.chat_histories(chat_history_query_dto=body)
        return result.data.to_dict()

    def reset_chat_history(self, character_id, user_id) -> bool:
        body = ResetChatHistoryRequest(characterId=character_id, userId=user_id)
        result = self.chat_message_api.reset_chat_history(request=body)
        return result.data
    
xingchen = XingChen(api_key="lm-bw72h4Q9oFOyuE47ncPxbg==")

# r = xingchen.chat(character_id="37d0bb98a0194eefbecdba794fb1b42c", message="那里不舒服？", seed=12345, user_id="123456789")
# st.write(r)

h = xingchen.get_chat_histories(character_id="37d0bb98a0194eefbecdba794fb1b42c",user_id="123456789", session_id="a020595ed022479bbad269ad69594382")
st.write(h)

# x = xingchen.reset_chat_history(character_id="37d0bb98a0194eefbecdba794fb1b42c",user_id="123456789")
# st.write(x)

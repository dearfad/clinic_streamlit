import streamlit as st
from xingchen import Configuration, ApiClient, ChatMessageApiSub, ChatHistoryQueryDTO, ChatHistoryQueryWhere, \
    MessageRatingRequest, SysReminderRequest


def init_client():
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = st.secrets["xingchen_token"]

    with ApiClient(configuration) as api_client:
        api_instance = ChatMessageApiSub(api_client)
    return api_instance

api = init_client()
body = ChatHistoryQueryDTO(
	where=ChatHistoryQueryWhere(
		characterId="37d0bb98a0194eefbecdba794fb1b42c",
		bizUserId="e22bde07e5e7418ca098a6c0462753c4",
		# sessionId="7ed48d9881b54ed49d6967be7be01743"
		# startTime="1970-01-01T00:00:00.00Z",
		# endTime="1970-01-01T00:00:00.00Z",
		# messageIds=[
		#     "e5bfc3c7809e47c5ac17181250adcf2b"
		# ],

	),
	orderBy=[
		"gmtCreate desc"
	],
	pageNum=1,
	pageSize=10
)

# 对话历史
result = api.chat_histories(chat_history_query_dto=body)
st.write(result.data)
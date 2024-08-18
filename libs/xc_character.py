import streamlit as st
from xingchen import (
    Configuration,
    ApiClient,
    CharacterApiSub,
    CharacterCreateDTO,
    FileInfoVO,
    CharacterAdvancedConfig,
    RepositoryInfo,
    Repository,
    CharacterPermissionConfig,
    CharacterQueryDTO,
    CharacterQueryWhere,
    CharacterUpdateDTO,
)


def init_client():
    configuration = Configuration(host="https://nlp.aliyuncs.com")
    configuration.access_token = st.secrets["xingchen_token"]

    with ApiClient(configuration) as api_client:
        api_instance = CharacterApiSub(api_client)
    return api_instance

# 角色详情
# api = init_client()
# result = api.character_details(character_id="37d0bb98a0194eefbecdba794fb1b42c").to_dict()
# st.write(result)

# 角色查询
# api = init_client()
# body = CharacterQueryDTO(
# 	where=CharacterQueryWhere(
# 		scope="my" # "my", "public", "pro_configured"
# 	),
# 	pageNum=1,
# 	pageSize=20,
# )
# result = api.search(character_query_dto=body).data.to_dict()
# st.write(result)
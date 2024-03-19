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
    CharacterVersionCreateOrUpdateDTO,
    CharacterQueryDTO,
    CharacterQueryWhere,
    CharacterUpdateDTO,
)

configuration = Configuration(host="https://nlp.aliyuncs.com")
configuration.access_token = "lm-bw72h4Q9oFOyuE47ncPxbg=="
with ApiClient(configuration) as api_client:
    api = CharacterApiSub(api_client)

body = CharacterQueryDTO(
    where=CharacterQueryWhere(
        # characterName="character_name_example",
        scope="pre_configured"
    ),
    # orderBy=[
    #     "order_by_example"
    # ],
    pageNum=1,
    pageSize=4,
)
result = api.delete(character_id="7e41634f145943a7a3289f2e958f63a5", version=1)
print(result.response.data)

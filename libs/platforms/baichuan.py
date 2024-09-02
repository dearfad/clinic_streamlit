import requests
import json


class BaiChuan:
    def __init__(self, api_key):
        self.url = "https://api.baichuan-ai.com/v1/chat/completions"
        self.api_key = api_key

    def chat(self, doctor, patient):
        data = {"model": patient.model.model, "messages": patient.messages, "stream": False}
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }
        response = requests.post(self.url, data=json_data, headers=headers, timeout=60)
        return json.loads(response.text)["choices"][0]["message"]["content"]

    # data = {
    #     "model": "Baichuan-NPC-Turbo",
    #     "character_profile": {"character_id": character_id},
    #     "messages": messages,
    #     "temperature": 0.8,
    #     "top_p": 0.98,
    #     "max_tokens": 512,
    #     "stream": False,
    # }
    # json_data = json.dumps(data)
    # headers = {"Content-Type": "application/json", "Authorization": "Bearer " + self.api_key}
    # response = requests.post(self.url, data=json_data, headers=headers, timeout=60)
    # return json.loads(response.text)['choices'][0]['message']['content']
    # if response.status_code == 200:
    #     print("请求成功！")
    #     print("响应body:", response.text)
    #     print("请求成功，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))
    # else:
    #     print("请求失败，状态码:", response.status_code)
    #     print("请求失败，body:", response.text)
    #     print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))


# if __name__ == "__main__":
#     baichuan = BaiChuan("sk-aa5e883004120ac5f07ec52d02b81b4b")
#     response = baichuan.chat(
#         character_id="30973",
#         messages=[
#             {"role": "user", "content": "你好"},
#             {"role": "assistant", "content": "大夫，你好"},
#             {"role": "user", "content": "哪里不舒服？"},
#         ],
#     )
#     print(json.loads(response.text)["choices"][0]["message"]["content"])

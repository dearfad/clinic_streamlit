from openai import OpenAI

API_BASE = "https://api.lingyiwanwu.com/v1"


class LingYi:
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key, base_url=API_BASE)

    def chat(self, doctor, patient):
        response = self.client.chat.completions.create(
            model=patient.model.model,
            messages=patient.messages,
        )
        # print(response)
        return response.choices[0].message.content

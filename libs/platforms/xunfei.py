from openai import OpenAI

class XingHuo:
    def __init__(self, api_key) -> None:        
        self.client = OpenAI(
                api_key=api_key, 
                base_url = 'https://spark-api-open.xf-yun.com/v1' # 指向讯飞星火的请求地址
            )
    def chat(self, doctor, patient):
        response = self.client.chat.completions.create(
            model='4.0Ultra', # 指定请求的版本
            messages=patient.messages
        )
        # print(response)
        return response.choices[0].message.content
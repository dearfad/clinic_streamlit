import os
import qianfan


class QianFan:
    def __init__(self, api_key):
        # os.environ["QIANFAN_ACCESS_KEY"] = "baiduid"
        os.environ["QIANFAN_SECRET_KEY"] = api_key
        self.client = qianfan.ChatCompletion()

    def chat(self, doctor, patient):
        response = self.client.do(
            model=patient.model.model, 
            messages=patient.messages[1:],
            system=patient.messages[0]['content'],
        )
        return response["body"]['result']

# -*- coding: utf-8 -*-
import json
import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

class HunYuan:
    def __init__(self, api_key):
        # self.cred = credential.Credential("tencentid", api_key)

        self.cpf = ClientProfile()
        # 预先建立连接可以降低访问延迟
        self.cpf.httpProfile.pre_conn_pool_size = 3
        self.client = hunyuan_client.HunyuanClient(self.cred, "ap-guangzhou", self.cpf)

    def chat(self, doctor, patient):
        messages = []
        for message in patient.messages:
            messages.append({key.title(): value for key, value in message.items()})
        req = models.ChatCompletionsRequest()
        params = {
            "Model": patient.model.model,
            "Messages": messages
        }
        req.from_json_string(json.dumps(params))
        response = self.client.ChatCompletions(req)

        return response.Choices[0].Message.Content

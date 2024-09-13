import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
import streamlit as st

tools = [
    {
        "Type": "function",
        "Function": {
            "Name": "get_report",
            "Description": "如果用户想看一下检查报告时应用",
            "Parameters": '{"type":"object", "properties":{"report":{"type":"string", "description":"检查报告，如：超声，血常规等"}}, "required":["report"]}',
        },
    }
]

def chat(patient):
    cred = credential.Credential(st.secrets["tencent_secret_id"], st.secrets['tencent_secret_key'])
    cpf = ClientProfile()
    # 预先建立连接可以降低访问延迟
    cpf.httpProfile.pre_conn_pool_size = 3
    client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", cpf)

    messages = []
    for message in patient.messages:
        messages.append({key.title(): value for key, value in message.items()})
    req = models.ChatCompletionsRequest()
    params = {
            "Model": patient.model.name,
            "Messages": messages,
            "Tools": tools,
        }
    req.from_json_string(json.dumps(params))
    response = client.ChatCompletions(req)
    # print(response.Choices[0].Message.ToolCalls)
    if response.Choices[0].Message.ToolCalls:
        tool_call = response.Choices[0].Message.ToolCalls[0].Function
        args = eval(tool_call.Arguments)
        if tool_call.Name == "get_report":
            return f"好的，这是我的{args['report']} ![](app/static/乳腺超声.jpg)"
    return response.Choices[0].Message.Content

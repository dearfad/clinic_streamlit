import os
import qianfan
import streamlit as st

func = [
    # 获取报告图片
    {
        "name": "get_report",
        "description": "如果用户想看一下检查报告时应用",
        "parameters": {
            "type": "object",
            "properties": {
                "report": {
                    "type": "string",
                    "description": "检查报告，如：超声，血常规等",
                },
            },
            "required": ["report"],
        },
    }
]


def chat(patient):
    os.environ["QIANFAN_ACCESS_KEY"] = st.secrets["baidu_access_Key"]
    os.environ["QIANFAN_SECRET_KEY"] = st.secrets["baidu_secret_key"]
    model = patient.model.name
    messages = patient.messages
    if model == "ERNIE-Functions-8K":
        response = qianfan.ChatCompletion().do(
            model=model,
            system=messages[0]["content"],
            messages=messages[1:],
            # temperature=0.95,
            # top_p=0.7,
            # functions=func,
            # This key `functions` does not seem to be a parameter that the model `ERNIE-Functions-8K` will accept
        )
        print(response["body"])
        return response["body"]["result"]
    else:
        response = qianfan.ChatCompletion().do(
            model=model,
            system=messages[0]["content"],
            messages=messages[1:],
            # temperature=0.95,
            # top_p=0.7,
        )
        return response["body"]["result"]

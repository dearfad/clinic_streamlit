import json

import requests
import streamlit as st
api_key = "lm-bw72h4Q9oFOyuE47ncPxbg=="
service_name = "aca-message-history"

url = "https://nlp.aliyuncs.com/v2/api/chat/message/histories"
headers = {
    "Content-Type": "application/json",
    "x-fag-servicename": service_name,
    "x-fag-appcode": "aca",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "where": {
        "characterId": "37d0bb98a0194eefbecdba794fb1b42c",
		"bizUserId": "123456",
        # "startTime": 1689783510026
    },
    "pageSize": 20,
    "orderBy": ["gmtCreate desc"]
}

response = requests.post(url, headers=headers, json=payload)
x = json.loads(response.text)
st.write(x['data']['list'][0]['content'])
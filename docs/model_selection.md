```mermaid
graph LR
    begin[大模型] ==> native[国内平台]
    begin ==> foreign[国外平台]

    native --> aliyun[阿里云 通义系列] 
    aliyun -->|角色扮演| xingchen[通义星辰]
    aliyun -->|通用| qianwen[通义千问]
    native --> bigmodel[智谱AI GLM系列]
    bigmodel -->|通用| glm4[GLM-4-Flash]
    bigmodel -->|角色扮演| charglm[CharGLM-3]
    native --> other[...平台]
    other --> model[...模型]
    foreign -.->|访问受限| OpenAI[ChatGPT]
    foreign -.->|访问受限| Anthropic[Claude]
    foreign -.->|访问受限| Google[Gemini]
    foreign -.-> other
  
```
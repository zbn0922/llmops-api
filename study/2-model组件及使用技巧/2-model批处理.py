#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/27 16:48
@description: 
"""
import os
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个KIMI聊天机器人，请根据用户的提问进行回复，当前的时间{now}"),
    HumanMessagePromptTemplate.from_template("{query}")
]).partial(now=datetime.now())

messages = chat_prompt.invoke({
    "query": "你好，你是?"
})
messages2 = chat_prompt.invoke({
    "query": "现在几点呀"
})

llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    temperature=0,  # 控制生成文本的随机性
    max_tokens=None,  # 最大生成长度，None 表示默认
    max_retries=2,  # 请求失败时重试次数
    base_url=os.getenv("OPENAI_BASE_URL"),
    # 也可以直接传入 api_key、base_url 等参数
)

ai_msg = llm.batch([
    messages,
    messages2,
])

for msg in ai_msg:
    print(msg.content)
    print(msg.response_metadata)
    print("==================")

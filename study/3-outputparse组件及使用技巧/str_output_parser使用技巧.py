#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/28 9:31
@description: 
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    temperature=0,  # 控制生成文本的随机性
    max_tokens=None,  # 最大生成长度，None 表示默认
    max_retries=2,  # 请求失败时重试次数
    base_url=os.getenv("OPENAI_BASE_URL"),
    # 也可以直接传入 api_key、base_url 等参数
)
chat_prompt_template = ChatPromptTemplate.from_template("{query}")

message = chat_prompt_template.invoke({"query": "你好，你是？"})
parser = StrOutputParser()
content = parser.invoke(llm.invoke(message))
print(content)

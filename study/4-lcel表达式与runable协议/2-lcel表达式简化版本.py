#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/28 11:18
@description: 
"""

import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    base_url=os.getenv("OPENAI_BASE_URL"),
)
parser = StrOutputParser()

chain = prompt | llm | parser

resp = chain.invoke({"query": "请讲一个程序员的冷笑话"})
print(resp)

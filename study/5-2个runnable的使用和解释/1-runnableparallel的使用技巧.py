#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/28 17:32
@description: 
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的笑话,尽可能短一些")
poem_prompt = ChatPromptTemplate.from_template("请做一首关于{subject}的诗,尽可能短一些")
llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    base_url=os.getenv("OPENAI_BASE_URL"),
)
parser = StrOutputParser()

joke_chain = joke_prompt | llm | parser
poem_chain = poem_prompt | llm | parser

# 并行链，并发执行这2个楝，目前月之暗面不支持并发
map_chain = RunnableParallel(
    {"joke": joke_chain, "poem": poem_chain}
)

res = map_chain.invoke({"subject": "程序员"})
print(res)

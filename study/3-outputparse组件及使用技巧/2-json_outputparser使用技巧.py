#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/28 9:45
@description: 
"""
import os

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class Joke(BaseModel):
    joke: str = Field(description="回答用户的冷笑话")
    punchline: str = Field(description="这个冷笑话的小店")


parser = JsonOutputParser(pydantic_object=Joke)

prompt = ChatPromptTemplate.from_template("请根据用户的提问进行回复\n{format_instructions}\n{query}").partial(
    format_instructions=parser.get_format_instructions())

message = prompt.format(query="请讲一个关于程序员的冷笑话")
print(message)

llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    temperature=0,  # 控制生成文本的随机性
    max_tokens=None,  # 最大生成长度，None 表示默认
    max_retries=2,  # 请求失败时重试次数
    base_url=os.getenv("OPENAI_BASE_URL"),
    # 也可以直接传入 api_key、base_url 等参数
)

joke = parser.invoke(llm.invoke(message))
print(joke)

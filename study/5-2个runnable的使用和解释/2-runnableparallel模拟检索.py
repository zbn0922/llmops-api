#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/28 17:47
@description: 
"""
# !/usr/bin/env python3
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


def retrieval(query: str) -> str:
    """模拟检索函数"""
    print("正在检索", query)
    return "我是张亮"


joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的笑话,尽可能短一些")
poem_prompt = ChatPromptTemplate.from_template("请做一首关于{subject}的诗,尽可能短一些")

prompt = ChatPromptTemplate.from_template("""请根据用户的提问回答，可以参考上下文

<context>
{context}
</context>

用户的提问是: {query}""")
llm = ChatOpenAI(
    model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
    base_url=os.getenv("OPENAI_BASE_URL"),
)
parser = StrOutputParser()
retrieval_chain = RunnableParallel({
    "context": lambda x: retrieval(x["query"]),
    "query": lambda x: x["query"]
})
chain = retrieval_chain | prompt | llm | parser

content = chain.invoke({"query": "我是谁"})
print(content)

# chain = prompt | llm | parser
# res = chain.invoke({"context": retrieval("你好我是谁"), "query": "我是谁"})
# print(res)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/27 10:54
@description: 
"""
from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (PromptTemplate,
                                    ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    MessagesPlaceholder
                                    )

prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")

print(prompt.format(subject="喜剧演员"))
prompt_value = prompt.invoke({"subject": "程序员"})
print(prompt_value.to_string())
print(prompt_value.to_messages())

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个KIMI聊天机器人，请根据用户的提问进行回复，当前的时间{now}"),
    MessagesPlaceholder("chat_history"),
    HumanMessagePromptTemplate.from_template("请讲一个序{subject}的冷笑话")
]).partial(now=datetime.now())
chat_prompt_value = chat_prompt.invoke({
    "chat_history": [
        ("human", "你好我是小张"),
        AIMessage("你好，我是kimi，请问我有什么可以帮您"),
        HumanMessage("有的呀， 你几岁了"),
        AIMessage("我10岁了")

    ],
    "subject": "程序员"
})
print(chat_prompt_value)
print(chat_prompt_value.to_string())

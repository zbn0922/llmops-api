#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/27 14:12
@description: 
"""

from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个KIMI聊天机器人，请根据用户的提问进行回复，我叫{username}")
    # SystemMessage("你是一个KIMI聊天机器人，请根据用户的提问进行回复，我叫{username}")
])

human_chat_prompt = ChatPromptTemplate.from_messages([
    # HumanMessage("{query}")
    ("human", "{query}")
])

chat_prompt = system_chat_prompt + human_chat_prompt
print(chat_prompt)

chat_prompt_value = chat_prompt.invoke({
    "username": "zhang liang",
    "query": "你好呀"
})

print(chat_prompt_value.to_string())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/5/6 16:13
@description: 
"""
import os

import dotenv
from langchain_community.chat_message_histories import (
    FileChatMessageHistory,
)
from openai import OpenAI

dotenv.load_dotenv()
chat_history = FileChatMessageHistory('./chat_history.json')
# chat_history.add_user_message("hi!")
#
# chat_history.add_ai_message("whats up?")

print(chat_history)

client = OpenAI(base_url=os.environ.get("OPENAI_API_URL"))
# 创建一个死循环用于人机对话
while True:
    # 获取人类的输入
    query = input('Human:')
    if query == 'q':
        break

    # 向openai的接口发起请求获取ai生成的内容
    answer_prompt = (
        "你是一个强大的聊天机器人，请根据对应的上下文和用户提问解决问题\n\n"
        f"<content>{chat_history}</content>\n\n"
    )
    response = client.chat.completions.create(
        model='moonshot-v1-8k',
        messages=[
            {"role": "system", "content": answer_prompt},
            {"role": "user", "content": query}
        ],
        stream=True,
    )
    print("AI: ", flush=True, end="")
    ai_content = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        ai_content += content
        print(content, flush=True, end="")
    print("")
    chat_history.add_user_message(query)
    chat_history.add_ai_message(ai_content)

# chat_history = InMemoryChatMessageHistory()
# chat_history.add_user_message("我叫张良，你是谁？")
# chat_history.add_ai_message("我是kimi，有什么可以帮助到您的？")
# print(chat_history)

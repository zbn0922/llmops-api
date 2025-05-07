#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/5/7 9:36
@description: 
"""
import os

import dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

dotenv.load_dotenv()

workflow = StateGraph(state_schema=MessagesState)

client = ChatOpenAI(model="moonshot-v1-8k", base_url=os.environ.get("OPENAI_API_URL"))


# Define the function that calls the model
def call_model(state: MessagesState):
    system_prompt = (
        "You are a helpful assistant. "
        "Answer all questions to the best of your ability."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = client.invoke(messages)
    return {"messages": response}


# Define the node and edge
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Add simple in-memory checkpointer
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 创建一个死循环用于人机对话
while True:
    # 获取人类的输入
    query = input('Human:')
    if query == 'q':
        break

    # 向openai的接口发起请求获取ai生成的内容
    response = app.stream(
        {"messages": [HumanMessage(content=query)]},
        config={"configurable": {"thread_id": "1"}},
    )

    print("AI: ", flush=True, end="")
    for msg in response:
        model_data = msg.get("model", {})
        ai_msg = model_data.get("messages")
        if ai_msg and ai_msg.type == "ai":
            print(ai_msg.content, flush=True, end="")
    print("")

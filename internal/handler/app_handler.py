#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/22 10:59
@description: 
"""
import os
import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, Any

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI

from internal.exception import NotFoundException
from internal.schma.app_schma import CompletionsReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """ 应用控制器 """
    app_service: AppService

    @classmethod
    def _load_memory_variables(cls, inputs: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """加载记忆变量信息"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(inputs)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存储对应的上下文信息到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: uuid.UUID):
        req = CompletionsReq()
        if not req.validate():
            return validate_error_json(req.errors)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问进行回答问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])

        memory = ConversationBufferWindowMemory(
            k=3,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.json"),
            input_key="query",
            output_key="output",
            return_messages=True,
        )

        # 连接大模型
        llm = ChatOpenAI(
            model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
            base_url=os.getenv("OPENAI_BASE_URL"),
        )

        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        input_val = {"query": req.query.data}
        content = chain.invoke(input_val, config={"configurable": {"memory": memory}})
        # memory.save_context(input_val, {"output": content})
        return success_json({"content": content})

        # # 构建提示词
        # prompt = ChatPromptTemplate.from_template("{query}")
        # # 连接大模型
        # llm = ChatOpenAI(
        #     model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
        #     base_url=os.getenv("OPENAI_BASE_URL"),
        # )
        # # 构建解释器
        # parser = StrOutputParser()
        # # 构造 LCEL 表达式
        # chain = prompt | llm | parser
        # content = chain.invoke({"query": req.query.data})
        # return success_json({"content": content})

    def create_app(self):
        app = self.app_service.create_app()

        return success_message(f"创建app数据成功，{app.name}, uuid:{app.id}")

    def get_app(self, app_id: uuid.UUID):
        app = self.app_service.get_app(app_id)

        return success_json(app.to_dict() if app is not None else {})

    def update_app(self, app_id: uuid.UUID):
        app = self.app_service.update_app(app_id)
        return success_json(app.to_dict() if app is not None else {})

    def delete_app(self, app_id: uuid.UUID):
        app = self.app_service.delete_app(app_id)
        return success_json(app.to_dict() if app is not None else {})

    def ping(self):
        raise NotFoundException("数据未找到")
        # return {"ping": "pong"}

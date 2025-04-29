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

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

    def debug(self, app_id: uuid.UUID):
        req = CompletionsReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 构建提示词
        prompt = ChatPromptTemplate.from_template("{query}")
        # 连接大模型
        llm = ChatOpenAI(
            model="moonshot-v1-8k",  # 指定模型名称，如 gpt-4o、gpt-3.5-turbo 等
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        # 构建解释器
        parser = StrOutputParser()
        # 构造 LCEL 表达式
        chain = prompt | llm | parser
        content = chain.invoke({"query": req.query.data})
        return success_json({"content": content})

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

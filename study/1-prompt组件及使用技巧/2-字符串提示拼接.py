#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/27 14:02
@description: 
"""

from langchain_core.prompts import PromptTemplate

prompt = (
        PromptTemplate.from_template("请讲一个关于{subject} 的冷笑话")
        + ",让我开心下\n"
        + "使用{language}语言"
)
prompt_value = prompt.invoke({
    "subject": "演员",
    "language": "中文"
})

print(prompt_value.to_string())

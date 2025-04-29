#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/27 14:25
@description: 
"""

import warnings

from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.pipeline import PipelinePromptTemplate

# 不展示弃用警告
warnings.simplefilter("ignore", category=DeprecationWarning)

full_prompt = PromptTemplate.from_template("""{introduction}

{example}

{start}""")

introduction_prompt = PromptTemplate.from_template("你正在模拟{username}")

example_prompt = PromptTemplate.from_template("""下面是一个交互的例子:

Q:{example_q}
A:{example_a}""")

start_prompt = PromptTemplate.from_template("""现在你是一个真人，请回答用户的问题：
Q:{input}
A:""")

pipline_template = [
    ("introduction", introduction_prompt),
    ("example", example_prompt),
    ("start", start_prompt)
]
pipline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=pipline_template)

print(pipline_prompt)

pipline_prompt_value = pipline_prompt.invoke({
    "username": "zl",
    "example_q": "最喜欢的汽车",
    "example_a": "斯柯达",
    "input": "最喜欢的手机？"
})

print(pipline_prompt_value.to_string())

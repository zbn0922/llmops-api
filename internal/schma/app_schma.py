#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/23 14:07
@description: 
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionsReq(FlaskForm):
    """基础请求参数验证"""
    query = StringField('query', validators=[
        DataRequired(message="用户的提问是必填的"),
        Length(max=2000),
    ])

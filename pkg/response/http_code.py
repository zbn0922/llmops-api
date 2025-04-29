#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/23 15:01
@description: 
"""
from enum import Enum


class HttpCode(str, Enum):
    # http 基本业务状态码
    SUCCESS = 'success'  # 成功
    FAIL = 'fail'  # 失败
    NOT_FOUND = 'not_found'  # 未找到
    UNAUTHORIZED = 'unauthorized'  # 未授权 （未登录）
    FORBIDDEN = 'forbidden'  # 无权限 （访问了不属于自己权限的资源）
    VALIDATION_ERROR = 'validation_error'  # 数据验证的错误

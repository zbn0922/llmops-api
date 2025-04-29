#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/23 15:06
@description: 
"""
from dataclasses import field, dataclass
from typing import Any

from flask import jsonify

from .http_code import HttpCode


@dataclass
class Response(object):
    code: HttpCode = HttpCode.SUCCESS
    message: str = ''
    data: Any = field(default_factory=dict)


def json(data: Response = None):
    return jsonify(data), 200


def success_json(data: Any = None):
    """ 成功数据响应 """
    return jsonify(Response(code=HttpCode.SUCCESS, message="", data=data)), 200


def fail_json(data: Any = None):
    """ 失败数据响应 """
    return jsonify(Response(code=HttpCode.FAIL, message="", data=data)), 200


def validate_error_json(errors: dict = None):
    """ 验证数据错误响应 """
    msg = ""
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]

    return jsonify(Response(code=HttpCode.VALIDATION_ERROR, message=msg, data=errors)), 200


def message(code: HttpCode = None, msg: str = ""):
    """基础的消息响应, 固定返回消息提示，数据固定为空字典"""
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ""):
    """成功的消息响应"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ""):
    """失败的消息响应"""
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ""):
    """失败的消息响应"""
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ""):
    """未授权的消息响应"""
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    """无权限的消息响应"""
    return message(code=HttpCode.FORBIDDEN, msg=msg)

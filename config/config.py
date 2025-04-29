#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/23 14:17
@description: 
"""
import os
from typing import Any

from .default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    # 从环境变量中获取配置项，如果找不到则获取默认值
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str) -> Any:
    # 从环境变量中获取布尔值配置项，如果找不到则获取默认值
    val: str = _get_env(key)
    return val.lower() == "true" if val is not None else "false"


class Config(object):
    """ flag 配置 """

    def __init__(self):
        # 关闭wtf 的 csrf
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED")

        # SQLAlchemy 配置
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            # 'pool_pre_ping': True,
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE")),
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),
        }
        self.SQLALCHEMY_ECHO = _get_bool_env("SQLALCHEMY_ECHO")

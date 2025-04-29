#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/25 15:13
@description: 
"""

# 应用默认配置项

DEFAULT_CONFIG = {
    # SQLAlchemy 数据库配置
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True",
    # wtf 的csrf配置
    "WTF_CSRF_ENABLED": "False"
}

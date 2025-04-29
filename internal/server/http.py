#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/22 11:18
@description: http 应用
"""
import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import Response, json, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    """ http 服务引擎"""

    def __init__(self,
                 *args,
                 conf: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs
                 ):
        super(Http, self).__init__(*args, **kwargs)
        # 注册配置文件
        self.config.from_object(conf)
        # 注册绑定异常处理
        self.register_error_handler(Exception, self._register_error_handler)
        # 初始化flask扩展  db
        db.init_app(self)
        # 初始化migrate
        migrate.init_app(self, db, "internal/migration")

        # with self.app_context():
        #     db.create_all()  # 创建所有使用到的表
        # 注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        print("异常", error)
        # 1、是否是自定义异常 ，如果是，可以提取code和message
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))
        # 2、如果不是自定义异常，也可以提取信息，转为FAIL异常
        if self.debug or os.getenv("DEBUG") == 'true':
            raise error
        else:
            return json(Response(
                code=HttpCode.FAIL,
                message=str(error),
                data={}
            ))

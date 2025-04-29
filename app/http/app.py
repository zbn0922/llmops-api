#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/22 11:22
@description: 
"""
import dotenv
from flask_migrate import Migrate
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from .module import ExtensionModule

# 将env文件中的内容加载到环境变量中
dotenv.load_dotenv()

conf = Config()
injector = Injector([ExtensionModule])
app = Http(__name__, conf=conf, migrate=injector.get(Migrate), db=injector.get(SQLAlchemy), router=injector.get(Router))

if __name__ == '__main__':
    app.run(debug=True)

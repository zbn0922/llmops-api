#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/25 16:53
@description: 
"""
import uuid
from dataclasses import dataclass

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        """应用服务逻辑"""
        with self.db.auto_commit():
            app = App(account_id=uuid.uuid4(), name='app1 test', description='这是一个简单的聊天机器人')
            self.db.session.add(app)
        return app

    def get_app(self, app_id: uuid.UUID) -> App:
        app = self.db.session.query(App).get(app_id)
        return app

    def update_app(self, app_id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(app_id)
            app.name = "第一次修改后的名称"

        return app

    def delete_app(self, app_id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(app_id)
            self.db.session.delete(app)
        return app

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/24 9:46
@description: 
"""
import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """ App 控制器 测试类"""

    @pytest.mark.parametrize("query", [None, "你好，你是？"])
    def test_completions(self, query, client):
        resp = client.post("/app/completions", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATION_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
        print("响应内容", resp.json)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhang liang
@date: 2025/4/21 17:07
@description: 
"""
from injector import Injector, inject


@inject
class B:
    def __init__(self, a: A):
        self.a = a


def main():
    # app = Flask()
    injector = Injector()
    b = injector.get(B)
    print(b, b.a.name)


if __name__ == '__main__':
    main()

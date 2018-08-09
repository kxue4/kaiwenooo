#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 17:14
# @Author  : Kaiwen Xue
# @File    : __init__.py
# @Software: PyCharm
from flask import Flask

app = Flask(__name__)
from app import views
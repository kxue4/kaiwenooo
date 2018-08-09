#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 17:15
# @Author  : Kaiwen Xue
# @File    : views.py
# @Software: PyCharm
from app import app
from app.boson_nlp import tag
from flask import render_template, request


# Index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# NLP index page
@app.route('/nlp', methods=['GET'])
def nlp_index():
    return render_template('nlp_index.html')


@app.route('/tags', methods=['POST'])
def tags():
    query = request.form['query']
    result = tag(query)
    limits = result[1]
    result_dict = result[0]
    return render_template('api_result_page.html',
                           title='Tag',
                           query=query,
                           result=str(result_dict),
                           limits=str(limits))


# API part
@app.route('/api/tag/<query>')
def got(query):
    result = tag(query)
    limits = result[1]
    result_dict = result[0]
    return render_template('api_result_page.html',
                           title='Tag',
                           query=query,
                           result=str(result_dict),
                           limits=str(limits))


# Error handler part
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
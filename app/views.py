#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 17:15
# @Author  : Kaiwen Xue
# @File    : views.py
# @Software: PyCharm
from app import app
from app.models import *
from flask import render_template, request


# Index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# NLP part
@app.route('/nlp', methods=['GET'])
def nlp():
    return render_template('nlp/nlp_index.html')


@app.route('/nlp/tag', methods=['POST'])
def nlp_tag():
    query = request.form['query']
    result = tag(query)
    limits = result[1]
    result_dict = result[0]  # {'再次': '副词', '测试': '动词', '字典': '名词'}
    tag_result = list()

    for key, value in result_dict.items():
        each_dict = {}
        each_dict['word'] = key
        each_dict['tag'] = value
        tag_result.append(each_dict)

    return render_template('nlp/nlp_tag_result.html',
                           query=query,
                           limits=str(limits),
                           tags=tag_result)


@app.route('/nlp/keywords', methods=['POST'])
def nlp_keywords():
    query = request.form['query']
    numbers = request.form['numbers']
    result = keywords(query, numbers)
    limits = result[1]
    result_list = result[0]  # [[0.6655955690669303, '提取'], [0.6075615797742268, '关键词'], [0.433418331312477, '测试']]
    keywords_result = list()

    for each in result_list:
        each_dict = {}
        each_dict['word'] = each[1]
        each_dict['percentage'] = each[0]
        keywords_result.append(each_dict)

    return render_template('nlp/nlp_keywords_result.html',
                           query=query,
                           limits=str(limits),
                           keywords=keywords_result)


@app.route('/nlp/sentiment', methods=['POST'])
def nlp_sentiment():
    cn2en = {'通用': 'general', '汽车': 'auto', '厨具': 'kitchen', '餐饮': 'food', '新闻': 'news', '微博': 'weibo'}
    query = request.form['query']
    cn_model = request.form['model']
    model = cn2en[cn_model]
    result = sentiment(query, model)
    limits = result[1]
    result_list = result[0]  # [0.96231491234, 0.037685088]
    pos = result_list[0]
    neg = result_list[1]

    return render_template('nlp/nlp_sentiment_result.html',
                           query=query,
                           limits=str(limits),
                           positive=pos,
                           negative=neg)


# Error handler part
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
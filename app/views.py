#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 17:15
# @Author  : Kaiwen Xue
# @File    : views.py
# @Software: PyCharm
from app import app
from app.models import *
from flask import render_template, request, redirect


# Index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/rss')
def rss():
    return redirect("http://www.kaiwenxue.com:1200", code=302)


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
        each_dict['left'] = key
        each_dict['right'] = value
        tag_result.append(each_dict)

    return render_template('nlp/nlp_result.html',
                           title='分词与词性标注',
                           is_form=1,
                           form_title_1='单词',
                           form_title_2='词性',
                           query=query,
                           limits=str(limits),
                           list=tag_result)


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
        each_dict['left'] = each[1]
        each_dict['right'] = each[0]
        keywords_result.append(each_dict)

    return render_template('nlp/nlp_result.html',
                           title='关键词提取',
                           is_form=1,
                           form_title_1='关键词',
                           form_title_2='权重',
                           query=query,
                           limits=str(limits),
                           list=keywords_result)


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
    sentiment_result = [{'left': '正面', 'right': pos}, {'left': '负面', 'right': neg}]

    return render_template('nlp/nlp_result.html',
                           title='情感分析',
                           is_form=1,
                           form_title_1='感情类型',
                           form_title_2='比例',
                           query=query,
                           limits=str(limits),
                           list=sentiment_result)


@app.route('/nlp/suggest', methods=['POST'])
def nlp_suggest():
    word = request.form['word']
    number = request.form['number']
    result = suggest(word, number)
    limits = result[1]
    suggest_dict = result[0]
    suggest_result = []

    for each in suggest_dict:
        each_dict = {}
        each_dict['left'] = each[1].split('/')[0]
        each_dict['right'] = each[0]
        suggest_result.append(each_dict)

    return render_template('nlp/nlp_result.html',
                           title='语义联想',
                           is_form=1,
                           form_title_1='联想词',
                           form_title_2='相似度',
                           query=word,
                           limits=str(limits),
                           list=suggest_result)


@app.route('/nlp/classify', methods=['POST'])
def nlp_classify():
    content = request.form['content'].strip()
    result = classify(content)
    limits = result[1]
    news_type = result[0]

    return render_template('nlp/nlp_result.html',
                           title='新闻分类',
                           is_form=0,
                           p1='分类结果:',
                           p2=news_type,
                           query=content,
                           limits=str(limits),
                           list=[])


@app.route('/nlp/summary', methods=['POST'])
def nlp_summary():
    content = request.form['content'].strip()
    title = request.form['title'].strip()
    result = summary(content, title)
    limits = result[1]
    summary_result = result[0]

    return render_template('nlp/nlp_result.html',
                           title='新闻摘要',
                           is_form=0,
                           p1='摘要内容:',
                           p2=summary_result,
                           query=content,
                           limits=str(limits),
                           list=[])


# Error handler part
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

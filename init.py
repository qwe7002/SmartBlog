#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import os.path

import memcache
from flask import Flask, abort, render_template

from common import file
from common import markdown

app = Flask(__name__)

# 分组页面
@app.route("/")
@app.route("/<file_name>")
@app.route("/<file_name>/")
@app.route('/<file_name>/page:<page>')
@app.route('/<file_name>/page:<page>/')
def route(file_name="index", page="1"):
    cache_pagename = file_name
    cache_result = get_cache("{0}/page:{1}".format(cache_pagename, str(page)))
    if cache_result is not None:
        return cache_result
    if file_name == "index":
        return build_index(int(page))
    if file_name == "rss" or file_name == "feed":
        return rss, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    if os.path.isfile("document/{0}.md".format(file_name)):
        return build_page(file_name)
    else:
        abort(404)


def build_index(page):
    Start_num = -system_config["Paging"] + (int(page) * system_config["Paging"])
    page_row_mod = divmod(len(page_list), system_config["Paging"])
    if page_row_mod[1] != 0 and len(page_list) > system_config["Paging"]:
        page_row = page_row_mod[0] + 2
    else:
        page_row = page_row_mod[0] + 1
    if page <= 0:
        abort(404)
    index_list = page_list[Start_num:Start_num + system_config["Paging"]]
    Document = render_template("./{0}/index.html".format(system_config["Theme"]), title="主页", menu_list=menu_list,
                               page_list=index_list,
                               system_config=system_config,
                               page_row=page_row - 1,
                               now_page=page, last_page=page - 1, next_page=page + 1)
    set_cache("index/page:{0}".format(str(page)), Document)
    return Document


def build_page(name):
    Document_Raw = file.read_file("document/{0}.md".format(name))
    if name in page_name_list:
        page_info = page_list[page_name_list.index(name)]
        content = Document_Raw
    else:
        Documents = Document_Raw.split("<!--infoend-->")
        page_info = json.loads(Documents[0])
        content = Documents[1]
    document = markdown.markdown(content)
    document = render_template("./{0}/post.html".format(system_config["Theme"]), title=page_info["title"],
                               page_info=page_info, menu_list=menu_list, content=document, system_config=system_config)
    set_cache(name, document)
    return document


def get_cache(pagename):
    if system_config["Cache"]:
        return mc.get(pagename)
    else:
        return None


def set_cache(page_name, content):
    if system_config["Cache"]:
        mc.set(page_name, content)


def get_item_name():
    item_list = []
    for page_item in page_list:
        item_list.append(page_item["name"])
    return item_list


page_list = json.loads(file.read_file("config/page.json"))
menu_list = json.loads(file.read_file("config/menu.json"))
system_config = json.loads(file.read_file("config/system.json"))
item_name_list = get_item_name()
page_name_list = list()
rss = file.read_file("document/rss.xml")

for item in page_list:
    page_name_list.append(item["name"])
if system_config["Cache"]:
    mc = memcache.Client([system_config["Memcached_Connect"]], debug=0)
    mc.flush_all()
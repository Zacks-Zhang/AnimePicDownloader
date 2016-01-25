# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib
import pubFunc
import threading
from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker
sys.path.append("pubFunc.py")

site = ""
safe = "http://Konachan.net/"
unsafe = "http://konachan.com/"
tags = []
count = 0
start_num = 1
pages_range = 1
pic_url_list = []

threads_num = 0


class ProgressBarThread(threading.Thread):
    """docstring for ProgressBarThread"""
    max_len = 0

    def __init__(self, len):
        super(ProgressBarThread, self).__init__()
        self.max_len = len


class DownLoadThread(threading.Thread):
    """docstring for DownLoadThread"""

    def __init__(self):
        super(DownLoadThread, self).__init__()


def InputSettings():
    global site, tags, start_num, pages_range
    print "=========Konachan Picture Downloader========="
    # Check if the failed file exists
    # If exists, ask user if resume last download.
    # ADD Check() && Resume()
    print "请输入tag, 多个tag请用空格隔开: "
    tag_temp = raw_input()
    tags = tag_temp.split(' ')
    print "需要安全模式吗?(y or else): "
    judge = raw_input()
    if judge == 'y' or judge == 'Y':
        site = safe
    else:
        site = unsafe
    print "请输入开始页码和页码范围, 数字间用空格隔开(例:1 100):"
    range_temp = raw_input().split(' ')
    start_num = (int)(range_temp[0])
    pages_range = (int)(range_temp[1])


def BuildIndexPageURL(index_num):
    ct_page_URL = site + "post.json?" + \
        "page=" + str(index_num) + "&tags="
    for tag in tags:
        ct_page_URL = ct_page_URL + "+" + tag
    return ct_page_URL


def BuildThreads(threads_num):
    threads = []
    progress_bar = ProgressBarThread(len(pic_url_list))
    threads.append(progress_bar)
    for i in range(0, threads_num):
        t = DownLoadThread()
        threads.append(t)
    return threads

InputSettings()

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
end_num = 1
index_page_url_list = []
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
    judge = true

    def __init__(self, TorF):
        super(DownLoadThread, self).__init__()
        self.judge = TorF

    def run(self):
        if judge:
            pass
        else:
            self.GetPicURL()

    def GetPicURL():
        global index_page_url_list
        lock = threading.Lock()
        while(index_page_url_list):
            lock.acquire()
            url = index_page_url_list.pop()
            lock.release()
            items = ParseJson(url)
            for single in items:
                lock.acquire()
                UpdatePicURLList(
                    {'id': single['id'], 'url': single['file_url']})
                lock.release()


def InputSettings():
    global site, tags, start_num, end_num, threads_num
    print "=========Konachan Picture Downloader========="
    ########################################
    # Check if the failed file exists
    # If exists, ask user if resume last download.
    # ADD Check() && Resume()
    ########################################
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
    end_num = (int)(range_temp[1]) + start_num
    print "请输入线程数量:"
    threads_num = (int)(raw_input())


def BuildAllPagesURL():
    global index_page_url_list
    for index_num in range(start_num, end_num):
        ct_page_URL = site + "post.json?" + "page=" + str(index_num) + "&tags="
        for tag in tags:
            ct_page_URL = ct_page_URL + "+" + tag
        index_page_url_list.append(ct_page_URL)


def ParseJson(index_page_url):
    page_content = pubFunc.OpenPage(pubFunc.BuildRequestGet(index_page_url))
    return json.loads(page_content)


def UpdatePicURLList(dict):
    global pic_url_list
    pic_url_list.append(dict)


def BuildThreads(threads_num):
    pass


def GetAllPicURL(self):
    print "正在获取链接...",
    print "OK!"


def Download(self):
    pass


if __name__ == '__main__':
    pass
else:
    pass

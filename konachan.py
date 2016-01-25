# -*- coding:utf-8 -*-
import urllib
import sys
import threading
import pubFunc
import json
from progressbar import Bar, ETA, Percentage, progressBar, RotatingMarker
sys.path.append("pubFunc.py")
sys.path.append("pubPara.py")

pic_url_list = []
progress = 0
safe = "http://Konachan.net/"
unsafe = "http://konachan.com/"
tags = []


class Konachan:
    site = ""
    start_page_num = 1
    pages_range = 1

    def __init__(self):
        global tags
        print "请输入tag, 多个tag请用空格隔开: "
        tag_temp = raw_input()
        tags = tag_temp.split(' ')
        print "需要安全模式吗?(y or else): "
        judge = raw_input()
        if judge == 'y' or judge == 'Y':
            self.site = safe
        else:
            self.site = unsafe
        print "请输入开始页码和页码范围, 数字间用空格隔开(例:1 100):"
        range_temp = raw_input().split(' ')
        self.start_page_num = (int)(range_temp[0])
        self.pages_range = (int)(range_temp[1])

    def BuildIndexPageURL(self, index_number):
        ct_page_URL = self.site + "post.json?" + \
            "page=" + str(index_number) + "&tags="
        for tag in tags:
            ct_page_URL = ct_page_URL + "+" + tag
        return ct_page_URL

    def BuildThreads(self, quantity, ):
        threads = []
        progress_bar = ProgressBarThread(len(pic_url_list))
        threads.append(progress_bar)
        for i in range(0, quantity):
            t = DownLoadThread(pic_file_dir)
            threads.append(t)
        return threads

    def GetAllPicURL(self):
        #
        print "正在获取链接...",
        print "OK!"

    def Download(self):
        self.GetAllPicURL()
        pic_file_dir = ""
        for tag in tags:
            pic_file_dir = pic_file_dir + tag + ' '
        pic_file_dir += '/'
        threads = self.BuildThreads()
        for t in threads:
            t.start()
        for t in threads:
            t.join()


class DownLoadThread(threading.Thread):
    pic_file_dir = ""

    def __init__(self, file_path):
        self.pic_file_dir = file_path
        threading.Thread.__init__(self)

    def run(self):
        self.Download()

    def Download(self):
        while(pic_url_list):
            thread_lock = threading.Lock()
            thread_lock.acquire()
            pic_url = pic_url_list.pop()
            thread_lock.release()
            try:
                self.DoDownload(pic_url)
            except:
                try:
                    self.DoDownload(pic_url)
                except:
                    try:
                        self.DoDownload(pic_url)
                    except:
                        error_file = open("error_file.txt", "ab")
                        error_file.write(urllib.unquote(pic_url) + '\n')
                        error_file.close
            finally:
                thread_lock.acquire()
                count += 1
                thread_lock.release()

    def DoDownload(self, pic_url):
        pic_file_name = self.FormatFileName(pic_url)
        pubFunc.SavePic(pubFunc.BuildRequestGet(pic_url), pic_file_name,
                        self.pic_file_dir)

    def FormatFileName(self, pic_url):
        unquoted_pic_url = urllib.unquote(pic_url)
        temp = unquoted_pic_url.split('/')
        file_name = temp[5]
        return file_name


class ProgressBarThread(threading.Thread):
    max_length = 0

    def __init__(self, length):
        self.max_length = length
        threading.Thread.__init__(self)

    def run(self):
        widgets = ['Downloading: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
                   ' ', ETA()]
        p_bar = progressBar(widgets=widgets, maxval=self.max_length).start()
        while(self.max_length - count):
            thread_lock = threading.Lock()
            thread_lock.acquire()
            p_bar.update(count)
            thread_lock.release()
        p_bar.finish()
        clean()


k = Konachan()
k.Download()

# TODO
# fix global name, such as: pic_file_dir..................None
# add prompt .............................................OK!
# create threads to get pic_urls..........................None

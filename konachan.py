# -*- coding:utf-8 -*-
import os
import sys
import shutil
import urllib
import urllib2
import pubFunc
import threading
import cPickle as pickle
from progressbar import Bar, Percentage, ProgressBar, RotatingMarker
sys.path.append("pubFunc.py")

####################
# global vars
count = 0
complete_tag = ""
pic_url_list = []
index_page_url_list = []
####################
# preference
site = ""
safe = "http://Konachan.net/"
unsafe = "http://konachan.com/"
tags = []
start_num = 1
end_num = 1
threads_num = 0
preference = {}


class ProgressBarThread(threading.Thread):
    """docstring for ProgressBarThread"""
    max_len = 0
    lock = threading.Lock()

    def __init__(self, len):
        super(ProgressBarThread, self).__init__()
        self.max_len = len
    # TODO:
    # Finish ProgressBarThread

    def run(self):
        widgets = ['Downloading: ', Percentage(), ' ', Bar(
            marker=RotatingMarker())]
        p_bar = ProgressBar(widgets=widgets, maxval=self.max_len).start()
        while(self.max_len - count):
            self.lock.acquire()
            p_bar.update(count)
            self.lock.release()
        p_bar.finish()


class CustomThread(threading.Thread):
    """docstring for DownLoadThread"""
    judge = True
    lock = threading.Lock()

    def __init__(self, TorF):
        super(CustomThread, self).__init__()
        self.judge = TorF

    def run(self):
        if self.judge:
            self.Download()
        else:
            self.GetPicURL()

    def GetPicURL(self):
        global pic_url_list, index_page_url_list
        fail_count = 0
        while(index_page_url_list):
            self.lock.acquire()
            url = index_page_url_list.pop()
            self.lock.release()
            items = self.Try3ParseJson(url)
            if items == {}:
                ++fail_count
            for single in items:
                if preference['safe'] and single['rating'] == "s":
                    self.lock.acquire()
                    pic_url_list.append(
                        {'id': single['id'], 'url': single['file_url']})
                    self.lock.release()
                elif not preference['safe']:
                    self.lock.acquire()
                    pic_url_list.append(
                        {'id': single['id'], 'url': single['file_url']})
                    self.lock.release()
        if fail_count != 0:
            print self.getName() + " 有" + str(fail_count) + "页打开失败"

    def Try3ParseJson(self, index_page_url):
        try:
            items = pubFunc.ParseJson(index_page_url)
            return items
        except:
            try:
                items = pubFunc.ParseJson(index_page_url)
                return items
            except:
                try:
                    items = pubFunc.ParseJson(index_page_url)
                    return items
                except:
                    SaveInfor(
                        complete_tag + ".jsonerror", 'ERROR/', index_page_url, 'ab')
                    return {}

    def Download(self):
        global pic_url_list, count
        fail_count = 0
        while(pic_url_list):
            self.lock.acquire()
            url_dict = pic_url_list.pop()
            url = url_dict['url']
            SaveInfor(complete_tag + '.temp', 'TEMP/', url, 'wb')
            self.lock.release()

            file_name = self.FormatFileName(url)
            fail_count += self.Try3SavePic(url, file_name)

            self.lock.acquire()
            count += 1
            self.lock.release()
        if fail_count != 0:
            print self.getName() + " 有" + str(fail_count) + "个图片下载失败"

    def Try3SavePic(self, url, file_name):
        try:
            pubFunc.SavePic(url, file_name)
            return 0
        except:
            try:
                pubFunc.SavePic(url, file_name)
                return 0
            except:
                try:
                    pubFunc.SavePic(url, file_name)
                    return 0
                except:
                    SaveInfor(
                        complete_tag + ".dlerror", 'ERROR/', url, 'ab')
                    return 1

    def FormatFileName(self, pic_url):
        unquoted_pic_url = urllib.unquote(pic_url)
        temp = unquoted_pic_url.split('/')
        file_name = temp[5]
        return file_name

####################
# utils


def GenerateTagStr():
    global complete_tag
    temp = ""
    for temp in tags:
        temp = temp + ' '
    complete_tag = temp[0:-1]


def SaveInfor(file_name, path, infor, mode):
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path + file_name):
        os.mknod(path + file_name)
        f = open(path + file_name, mode)
        pickle.dump(preference, f, True)
        pickle.dump(infor, f, True)
        f.close()
    else:
        f = open(path + file_name, mode)
        pickle.dump(infor, f, True)
        f.close()

####################
# main functions


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
    GenerateTagStr()
    preference['tags'] = tags
    print "需要安全模式吗?(y or else): "
    judge = raw_input()
    if judge == 'y' or judge == 'Y':
        site = safe
        preference['safe'] = True
    else:
        site = unsafe
        preference['safe'] = False
    print "请输入开始页码和页码范围, 数字间用空格隔开(例:1 100):"
    range_temp = raw_input().split(' ')
    start_num = (int)(range_temp[0])
    end_num = (int)(range_temp[1]) + start_num
    preference['start_num'] = start_num
    preference['end_num'] = end_num
    print "请输入线程数量:"
    threads_num = (int)(raw_input())
    preference['threads_num'] = threads_num


def ChangeDir():
    if not os.path.exists(complete_tag):
        os.mkdir(complete_tag)
    os.chdir(complete_tag)


def BuildAllPagesURL():
    global index_page_url_list
    for index_num in range(start_num, end_num):
        ct_page_URL = site + "post.json?" + "page=" + str(index_num) + "&tags="
        for tag in tags:
            ct_page_URL = ct_page_URL + "+" + tag
        index_page_url_list.append(ct_page_URL)


def StartGetPicURLThreads():
    print "正在获取图片链接......"
    threads = []
    for i in range(0, threads_num):
        ct_thread = CustomThread(False)
        ct_thread.start()
        threads.append(ct_thread)
    for ct_thread in threads:
        ct_thread.join()


def StartDownloadThreads():
    print "开始下载......"
    threads = []
    p_bar = ProgressBarThread(len(pic_url_list))
    threads.append(p_bar)
    p_bar.start()
    for i in range(0, threads_num):
        ct_thread = CustomThread(True)
        ct_thread.start()
        threads.append(ct_thread)
    for ct_thread in threads:
        ct_thread.join()
    # TODO:
    # add progressbar


def RemoveTempFiles():
    if os.exists('TEMP'):
        shutil.rmtree('TEMP')


def main():
    InputSettings()
    ChangeDir()
    BuildAllPagesURL()
    StartGetPicURLThreads()
    # waiting GetPicURLThreads exit...
    StartDownloadThreads()
    RemoveTempFiles()


if __name__ == '__main__':
    main()
else:
    pass

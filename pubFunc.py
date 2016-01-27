# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json


def BuildRequestPost(URL, values={}, headers={}):
    data = urllib.urlencode(values)
    request = urllib2.Request(URL, data, headers)
    return request


def BuildRequestGet(URL):
    request = urllib2.Request(URL)
    return request


def OpenPage(page_url_request):
    response = urllib2.urlopen(page_url_request)
    page = response.read()
    return page


def ParseJson(index_page_url):
    page_content = OpenPage(BuildRequestGet(index_page_url))
    return json.loads(page_content)


def FindPicURLbyRE(page_content, target):
    pattern = re.compile(target, re.S)
    pic_URL_list = pattern.findall(pattern, page_content)
    return pic_URL_list


def SavePic(pic_URL_request, file_name, file_dir=""):
    if not file_dir == "":
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
    response = urllib2.urlopen(pic_URL_request)
    pic_content = response.read()
    pic = open(file_dir + file_name, 'wb')
    pic.write(pic_content)
    pic.close()

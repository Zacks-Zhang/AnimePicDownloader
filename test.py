# -*- coding:utf-8 -*-

a = 3
print a


def x():
    global a
    a = 4
x()
print a

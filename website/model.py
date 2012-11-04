# -*- coding: utf-8 -*-

class Status:
    """ 微博类 """
    def __init__(self, uid=0, touid=0, content=''):
        self.uid = uid
        self.touid = touid
        self.content = content

class Message:
    """ 私信类 """
    def __init__(self):
        pass
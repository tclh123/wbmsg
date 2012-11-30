# -*- coding: utf-8 -*-

class Message:
    """ 私信类 """
    def __init__(self, uid='', touid='', type=0, content='', time=''):
        self.uid = uid
        self.touid = touid
        self.type = type    # 0:send, 1:receive
        self.content = content
        self.time = time

class Status:
    """ 微博类 """
    def __init__(self, uid='', touid='', content=''):
        self.uid = uid
        self.touid = touid
        self.content = content
        #    def __str__(self):
        #        return "uid=%d, touid=%s, content=%s" % (self.uid, self.touid, self.content)
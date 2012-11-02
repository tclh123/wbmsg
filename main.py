#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
import services

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

render = web.template.render('templates')

urls = (
    '/(|list)', 'list',
    '/(new|send)', 'new',
    '/chat', 'chat',
    '/del', 'destroy',
    )

#   TODO： GAE 怎么用 hook？是 web.header()在GAE上无效啊?...为毛
#def customhook():
#    web.header("Content-type","text/html; charset=utf-8")
#web.application(urls, globals()).add_processor(web.loadhook(customhook))

class index:
    def GET(self):
        """
        wbmsg. ver - 1.0
        usage:
        读取：GET
        写入：POST
        ----
        token -> cookie: gsid_CTandWM, 能否通过 uid,pwd 登陆获得?: TODO.
        """
        return 'welcome to wbmsg | code by tclh123'

#########################
#   Page handles
#########################

#
#   /list: 获取个人私信列表
#       GET(uid, token) return json(list<message>)
#
class list:
    def GET(self, url):
        web.header("Content-type","text/html; charset=utf-8")
        i = web.input(uid=0, token=0)
        statuses = services.get_messages(i.uid, i.token)      # TODO 完成自定义类 的json解析
        return json.dumps(statuses, ensure_ascii=False) #加了 ensure_ascii，编码终于显示正常

#
#   /new: 发送私信
#       POST(uid, token, text, touid) return 1
#
class new:
    """ e.g. /new?uid=1903362107&token=3_58ac1a8401cf4825abacad4c983f2c5080b1e8&touid=1659177872&text=testlo """
    def GET(self, url):
        i = web.input(uid=0, token=0, touid=0, text=0)       #TODO 删掉
        services.post_message(i.uid, i.token,  i.touid, i.text)

        return '/(new|send): pls use POST to send new message.'
    def POST(self, url):
        i = web.input(uid=0, token=0, touid=0, text=0)
        services.post_message(i.uid, i.token,  i.touid, i.text) #TODO 这里post的东西会不会导致 urlencode两次？
        return 'new'    #TODO 修改返回值

#
#   /chat: 获取个人与某用户的所有私信（聊天列表）
#       GET(uid, token, touid) return json(list<message>)
#
class chat:
    """ e.g. /chat?uid=1903362107&token=3_58ac1a8401cf4825abacad4c983f2c5080b1e8&touid=1659177872 """
    def GET(self):
        web.header("Content-type","text/html; charset=utf-8")
        i = web.input(uid=0, token=0, touid=0)
        statuses = services.message_chat(i.uid, i.token, i.touid)
        return statuses

#
#   /del:  删除个人与某用户的所有私信（于weibo.com服务器上）
#       POST(uid, token, touid)
#
class destroy:
    """ e.g. /del?uid=1903362107&token=3_58ac1a8401cf4825abacad4c983f2c5080b1e8&touid=1659177872 """
    def GET(self):
        i = web.input(uid=0, token=0, touid=0)
        services.del_status(i.uid, i.token, i.touid)
        return '/del: pls use POST to del messages with certain to-user.'
    def POST(self):
        i = web.input(uid=0, token=0, touid=0)
        services.del_status(i.uid, i.token, i.touid)
        return 'del'

app = web.application(urls, globals()).wsgifunc()
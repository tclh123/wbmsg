#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import httphelper
import config
import util
import model

#TODO 各function协议返回值

def handle_status(uid, token, status):
    """处理微博并发送，处理多条发送"""
    http = httphelper.HttpHelper()
    # set cookies and gsid
    http.add_cookie('_WEIBO_UID', uid, '.weibo.cn')
    http.add_cookie('_T_WL', '1', '.weibo.cn')
    http.add_cookie('gsid_CTandWM', token, '.weibo.cn')
    # logging.debug(http.cj)

    #make url_post
    try:
        html_main = http.get(config.URL_WEIBO)
        pa_st = re.compile(r'(.*?)st=(.*?)&')     # 不知道为什么这里会匹配到st后面的信息..
        m = pa_st.match(html_main)
        st = m.group(2)    #/mblog/sendmblog?st=1ad7&amp;st=1ad7&amp;vt=4&amp;gsid=3_58ac1a8401cf4825abacad4c983f2c5080b1e8
        st = st[0:4]
        url_post = '%s?%s' % (config.URL_POST, httphelper._encode_params(gsid = token,
            st = st,
            vt = 4))
    except:
        e = 'failed to MAKE url_post', util.str_time()
        logging.info(e)

    maxlen = config.STATUS_MAXLEN * 3
    if len(status) > maxlen:   #分条发送
        length = maxlen-3*5
        n = len(status)/length + 1
        for j in range(0, n):
            _post_status(http, url_post, '['+str(j+1)+'/'+str(n)+']' + status[j*length:j*length+length])
    else:
        _post_status(http, url_post, status[0:420])   #3倍

def _post_status(http, url_post, status='invalid message'):
    """发微薄"""
    logging.warning(status)

    http.post(url_post,
        content = status,
        rl = 0)

def del_status(uid, token, touid):  #TODO： 把status改成message.
    """删除私信"""
    logging.debug(touid)
    http = httphelper.HttpHelper()
    # set cookies and gsid
    http.add_cookie('_WEIBO_UID', uid, '.weibo.cn')
    http.add_cookie('_T_WL', '1', '.weibo.cn')
    http.add_cookie('gsid_CTandWM', token, '.weibo.cn')
    http.get(config.URL_MSG_DEL + touid + '?&do=del&&rl=0')

def get_messages(uid, token):
    #TODO: 现在只是获取第一页私信列表，并且是每个对话的最近一条(而且没判断是发送的还是接受的)。要改成获取每页私信（每个对话最近条即可）。

    http = httphelper.HttpHelper()
    # set cookies and gsid
    http.add_cookie('_WEIBO_UID', uid, '.weibo.cn')
    http.add_cookie('_T_WL', '1', '.weibo.cn')
    http.add_cookie('gsid_CTandWM', token, '.weibo.cn')

    try:
        #get all msgs
        html = http.get(config.URL_MSG)
    except:
        e = 'failed to GET msg', util.str_time()
        logging.info(e)
    try:
        #parse statuses
        statuses = []
        idx = 0
        pa_status = re.compile(r'说:(.*?)&nbsp;<span class="ct">')
        pa_touid = re.compile(r'/im/callchat\?uid=(\d+)')
        for status in re.findall(pa_status, html):
            #statuses.append(model.Status(content = status))
            statuses.append(status)
#        for touid in re.findall(pa_touid, html):
#            statuses[idx].touid = touid     #TODO
#            idx += 1
    except:
        e = 'failed to PARSE statuses', util.str_time()
        logging.info(e)

    return statuses

def post_message(uid, token, touid, text):
    # URL_MSG_POST

    http = httphelper.HttpHelper()
    # set cookies and gsid
    http.add_cookie('_WEIBO_UID', uid, '.weibo.cn')
    http.add_cookie('_T_WL', '1', '.weibo.cn')
    http.add_cookie('gsid_CTandWM', token, '.weibo.cn')

    html = http.post(config.URL_MSG_POST,
        content = text,
        rl = 1,
        uid = touid)
    #TODO 看302之后的html，有"发送成功"字样没，修改函数返回值

def message_chat(uid, token, touid):
    # ?uid=1659177872

    http = httphelper.HttpHelper()
    # set cookies and gsid
    http.add_cookie('_WEIBO_UID', uid, '.weibo.cn')
    http.add_cookie('_T_WL', '1', '.weibo.cn')
    http.add_cookie('gsid_CTandWM', token, '.weibo.cn')

    html = http.get(config.URL_MSG_Chat + '?type=record&uid=' + touid)
    """
与逆风soso的聊天记录 清空
我:试试8分钟前  转发
我:testlo12分钟前  转发
我:发送测试啦50分钟前  转发
我:给逆风啦10月16日 23:26  转发
我:test10月15日 16:18  转发
逆风soso:测试下啦啦啦啦03月31日 22:21  转发
    """
    return html #TODO，正则获得私信列表
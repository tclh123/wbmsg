#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import httphelper
import config
import util
import model

#TODO 各function协议返回值

#########################
#   Main Services
#   (del,get,post,list,login)
#########################

def login(username, password):
    """ 登陆3g.sina.com.cn，返回uid，token(gsid_CTandWM)，失败返回None """
    http = httphelper.HttpHelper({
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding' : 'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'3g.sina.com.cn',
        'Origin':'http://3g.sina.com.cn',
        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
    })
    http.add_cookie('Apache', '000000e6.6a551ca5.506f3329.72ef223f', '')    # 后来测了下这些cookie好像没用？
    http.add_cookie('_s_upa', '1', '')
    http.add_cookie('SINAGLOBAL', '000000e6.6a5a1ca5.506f3329.f4261ad5', '')
    http.add_cookie('SessionID', '4pqfvhtunbbrklsfhlojqcrqi2', '')
    http.add_cookie('ULOGIN_IMG', '5ce6ac5dfea59efa4cdff5bd07780801bf7b', '')
    http.add_cookie('U_TRS1', '00000081.c89d3d52.506bf86c.43727748', '')
    http.add_cookie('U_TRS2', '000000a9.7fb221f7.509c6a26.59abba49', '')
    http.add_cookie('ALF', '1353057279', '')
    http.add_cookie('SUR', 'uid%3D1659177872%26user%3D15988481268.cn%26nick%3D15988481268%26email%3D15988481268%2540sina.cn%26dob%3D%26ag%3D8%26sex%3D%26ssl%3D0', '')
    http.add_cookie('SUS', 'SID-1659177872-1352534414-XD-7uf03-50928f47b12632b5cbfe0e415865117e', '')
    http.add_cookie('SINABLOGNUINFO', '1659177872.62e50b90.', '')

    html = http.get(config.URL_LOGIN)

    pa_pwd = re.compile(r'(.*?)type="password" name="(.*?)"', re.S)	#加re.S，使.能匹配换行符
    m = pa_pwd.match(html)
    pwd_with_code = m.group(2)

    pa_vk = re.compile(r'(.*?)name="vk" value="(.*?)"', re.S)
    m = pa_vk.match(html)
    vk = m.group(2)

    params = {
        'mobile' : username,
        'remember' : 'on',
        'vk' : vk,
        'submit' : '登录'
    }
    params[pwd_with_code] = password
    http.post(config.URL_LOGIN, **params)
    token = http.get_cookie_value('gsid_CTandWM')
    http.get(config.URL_WEIBO,
        gsid=token,
        vt=4,
        lret=1
    )
    uid = http.get_cookie_value('_WEIBO_UID')
    return uid, token

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

#########################
#   Extra
#########################

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
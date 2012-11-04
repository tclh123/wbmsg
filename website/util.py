#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from google.appengine.api import mail

def str_time():
    """时间字符串"""
    return time.strftime('[%H:%M:%S]')

def send_mail(msg):
    """发邮件"""
    message = mail.EmailMessage(
        sender  = 'tclh123@gmail.com',
        subject = "XduSecret's Notice from GAE")
    message.to  = '376458021@qq.com'
    message.body= """
        Hello Harry:
            XduSecret's Notice: %s
            //THE END.
            %s.
                  """ % (msg, time.ctime())
    message.send()
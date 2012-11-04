#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import logging
import cookielib
import re
from google.appengine.api import urlfetch

def _encode_params(**kw):
    """ Encode parameters. """
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        if k == 'mobile':   # 当时是为了pwd特殊处理下，貌似没用了
            args.append('%s=%s' % (k, qv))
        else:
            args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

class HttpHelper:
#    # create
#    http = HttpHelper()
#    # set cookies and gsid
#    http.add_cookie('_WEIBO_UID', WEIBO_UID, '.weibo.cn')
#    http.add_cookie('_T_WL', '1', '.weibo.cn')
#    http.add_cookie('gsid_CTandWM', COOKIE, '.weibo.cn')
#    gsid = COOKIE
    """ Http 封装类 """
    def __init__(self):
        self.cj = cookielib.CookieJar()
    def get(self, url, **kw):
        logging.debug('GET %s' % url)
        return self._http_call(url, urlfetch.GET, **kw)
    def post(self, url, **kw):
        logging.debug('POST %s' % url)
        return self._http_call(url, urlfetch.POST, **kw)
    def add_cookie(self, name, value, domain):
        ck = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ck)
    def _http_call(self, url, method, **kw):
        params = _encode_params(**kw)   #params is a str
        if method == urlfetch.GET:
            http_url = '%s?%s' % (url, params) if params!='' else url
            http_body = None
        else:
            http_url = url
            http_body = params
        resp = urlfetch.fetch(url=http_url,
            payload=http_body,
            method=method,
            headers=self._getHeaders(self.cj),
            deadline=10
        )
        # Load the cookies from the response
        # 顺便把domain都换成.weibo.cn
        # e.g. gsid_CTandWM=3_58ac1a8401cf4825abacad4c983f2c5080b1e8; expires=Tue, 01-May-2012 16:29:23 GMT; path=/; domain=.sina.com.cn
        # e.g. resp.headers.get('set-cookie') = 'gsid_CTandWM=deleted; expires=Sat, 02-Apr-2011 16:35:07 GMT; path=/; domain=.sina.com.cn'
        str_set_ck = resp.headers.get('set-cookie')
        if str_set_ck:
            m = re.match(r'(.*?)=(.*?);', str_set_ck)
            if m:
                if m.group(2) != 'deleted':
                    self.add_cookie(m.group(1), m.group(2), '.weibo.cn')
        return resp.content
    def _getHeaders(self, cj):
        headers = {
            'Accept-Encoding' : 'utf-8',
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Cookie' : self._makeCookieHeader(cj)
        }
        return headers
    def _makeCookieHeader(self, cj):
        """ cookielib.CookieJar to str_Cookie """
        cookieHeader = ""
        for i in cj._cookies.itervalues():
            for j in i['/'].itervalues():
                cookieHeader += '%s=%s;' % (j.name, j.value)
        return cookieHeader

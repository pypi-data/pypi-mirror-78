#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _base .py
# @time: 2020/8/30 6:52
# @Software: PyCharm

from snowland_authsdk.login import Account
import requests
from qywechat.common import GETTOKEN_URL


class BaseClient(Account):
    def __init__(self, corpid, corpsecret):
        super(BaseClient, self).__init__(corpid, corpsecret)
        self._token = self.get_token()

    @property
    def corpid(self):
        return self.access_key

    @property
    def corpsecret(self):
        return self.access_secret

    def get_token(self):
        url = GETTOKEN_URL.format(corpid=self.corpid, corpsecret=self.corpsecret)
        try:
            res = requests.get(url).json()
            token = res['access_token']
            return token
        except Exception:
            raise Exception('获取token异常')

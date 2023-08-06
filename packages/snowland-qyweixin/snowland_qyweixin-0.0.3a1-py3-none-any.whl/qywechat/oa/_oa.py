#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: _oa .py
# @time: 2020/8/30 16:35
# @Software: PyCharm


from qywechat.base import BaseClient
from qywechat.common import OA_GETAPPROVALDETAIL_URL, OA_GETAPPROVALINFO_URL
import requests
import datetime


class OAClient(BaseClient):

    def __init__(self, corpid, corpsecret, appid):
        super(OAClient, self).__init__(corpid, corpsecret)
        self.appid = appid

    def get_approval_detail(self, sp_no, parser=None):
        """
        :param sp_no:
        :param parser: 解析器，把返回的数据解析到特定格式
        :return:
        """
        token = self.get_token()
        detail_url_with_token = OA_GETAPPROVALDETAIL_URL.format(token=token)
        data = {
            'sp_no': sp_no
        }
        detail_res = requests.post(detail_url_with_token, json=data)
        details = detail_res.json()
        if parser is not None:
            return parser(details)
        return details

    def get_approval_info(self,
                          start_time=None,
                          end_time=None,
                          cursor=0,
                          size=100,
                          template_id=None,
                          creator=None,
                          department=None,
                          sp_status=None,
                          parser=None,
                          time_delta=3600):
        """
        :param start_time:
        :param end_time:
        :param parser: 解析器，把返回的数据解析到特定格式
        :return:
        """
        token = self.get_token()
        url = OA_GETAPPROVALINFO_URL.format(token=token)
        if end_time is None:
            end_time = int(datetime.datetime.now().timestamp())
        elif isinstance(end_time, datetime.datetime):
            end_time = int(end_time.timestamp())
        if start_time is None:
            start_time = end_time - time_delta
        elif isinstance(start_time, datetime.datetime):
            start_time = int(end_time.timestamp())
        filters = []
        if template_id:
            filters.append(dict(key="template_id", value=template_id))
        if creator:
            filters.append(dict(key="creator", value=creator))
        if department:
            filters.append(dict(key="department", value=department))
        if sp_status:
            filters.append(dict(key="sp_status", value=sp_status))
        data = {
            "starttime": str(start_time),
            "endtime": str(end_time),
            "cursor": cursor,
            "size": size,
            "filters": filters
        }
        res = requests.request(url, json=data)
        li = res["sp_no_list"]
        if parser is not None:
            return parser(li)
        return li

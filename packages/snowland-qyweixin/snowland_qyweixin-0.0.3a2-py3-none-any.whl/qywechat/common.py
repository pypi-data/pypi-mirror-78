#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: common .py
# @time: 2020/8/30 6:42
# @Software: PyCharm


GETTOKEN_URL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'

DETAIL_STATE_MAP = {
    1: '审批中',
    2: '已同意',
    3: '已驳回',
    4: '已转审',
    7: '未知状态'
}

OA_GETAPPROVALINFO_URL = 'https://qyapi.weixin.qq.com/cgi-bin/oa/getapprovalinfo?access_token={token}'
OA_GETAPPROVALDETAIL_URL = 'https://qyapi.weixin.qq.com/cgi-bin/oa/getapprovaldetail?access_token={token}'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: serializer .py
# @time: 2020/9/2 16:58
# @Software: PyCharm


import time
from qywechat.common import DETAIL_STATE_MAP
def item_to_string(x):
    """
    控件转String
    :param x: 控件dict
    :return: 转化过后的string
    """
    if x['control'] == 'Text':
        val = '{}:{}'.format(x['title'][0]['text'], x['value'].get('text'))
    elif x['control'] == 'Date':
        val = '{}:{}'.format(x['title'][0]['text'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            int(x['value']['date']['s_timestamp']))))
    elif x['control'] == 'Selector':
        val = '{}:{}'.format(x['title'][0]['text'], x['value']['selector']['options'][0]['value'][0]['text'])
    elif x['control'] == 'Textarea':
        val = '{}:{}'.format(x['title'][0]['text'], x['value']['text'])
    elif x['control'] == 'Contact':
        val = '{}:{}'.format(x['title'][0]['text'], [m['name'] for m in x['value']['members']])
    elif x['control'] == 'Number':
        val = '{}:{}'.format(x['title'][0]['text'], x['value']['new_number'])
    elif x['control'] == 'Tips':
        val = '成功获取所有信息'
    elif x['control'] == 'Table':
        if x['value']['children']:
            vaa = []
            for h in x['value']['children']:
                vak = [item_to_string(v) for v in h['list']]
                vaa.append("[{}]".format(','.join(vak)))
            val = '{}:{}'.format(x['title'][0]['text'], '[{}]'.format(','.join(vaa)))
        else:
            val = '暂无信息'
    elif x['control'] == 'Money':
        val = '{}:{}'.format(x['title'][0]['text'], x['value'].get('new_money'))
    elif x['control'] == 'File':
        val = '{}:[{}]'.format(x['title'][0]['text'], ','.join([f['file_id'] for f in x['value']['files']]))
    else:
        val = '{}:{}'.format(x['title'][0]['text'], x['value'].get('tips'))
    return val


def info_to_dict(details):
    """
    控件提取信息
    :param details: 控件返回的json
    :return:
    """
    infos = {
        '审批编号': details["info"]["sp_no"],
        '模板ID': details['info']['template_id'],
        '审批名称': details["info"]["sp_name"],
        '审批状态': DETAIL_STATE_MAP[details["info"]["sp_status"]],
        '审批提交时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(details["info"]["apply_time"])),
        '审批意见': details["info"]["sp_record"][0]["details"][0]["speech"],
        '控件信息': [item_to_string(x) for x in details["info"]["apply_data"]["contents"]]
    }
    return infos

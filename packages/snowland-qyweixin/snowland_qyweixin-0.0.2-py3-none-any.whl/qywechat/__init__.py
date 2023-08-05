#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: __init__.py .py
# @time: 2020/8/30 6:35
# @Software: PyCharm

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: setup.py
# @time: 2018/9/8 1:31
# @Software: PyCharm

from astartool.setuptool import get_version

version = (0, 0, 2, 'final', 0)
__version__ = get_version(version)

del get_version

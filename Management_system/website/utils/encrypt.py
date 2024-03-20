#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/20 16:40
# @Author  : Aries
# @File    : encrypt.py
# @Description : MD5加密
from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 加点'盐'
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

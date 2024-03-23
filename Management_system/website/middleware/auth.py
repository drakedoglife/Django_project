#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/23 22:58
# @Author  : Aries
# @File    : auth.py.py
# @Description : 中间件
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, reverse


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的界面
        # request.path_info 获取当前用户请求的URL
        if request.path_info == '/login/':
            return None

        # 1.读取当前用户的session信息，如果能读到说明已经登录
        info_dict = request.session.get('info')
        if info_dict:
            return None
        # 没有登录过，就告诉用户请登录
        return redirect(reverse('login'))

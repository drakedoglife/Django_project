#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/21 15:48
# @Author  : Aries
# @File    : account.py
# @Description : 登录页面视图函数
from django.shortcuts import render, redirect, reverse, HttpResponse
from website import models
from website.utils.form import LoginForm


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)

    if form.is_valid():
        # 验证成功
        print(form.cleaned_data)
        return HttpResponse("提交成功")
    return render(request, 'login.html', {'form': form})

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/21 15:48
# @Author  : Aries
# @File    : account.py
# @Description : 登录页面视图函数
from django.shortcuts import render, redirect, reverse, HttpResponse
from website import models
from website.utils.form import LoginForm
from website.utils.imgcheck import check_code
from io import BytesIO


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)

    if form.is_valid():
        # 验证成功
        # 去数据库校验用户名密码是否正确，如果错误，获取None

        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code_dict = request.session.get('image_code', "")
        if code_dict['code'].upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串，写到浏览器的cookie，写到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect(reverse('admin_list'))
    return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect(reverse('login'))


def image_code(request):
    """生成验证码图片"""
    # 调用pillow生成验证码
    img, code_str = check_code()
    # 将验证码文字写入session
    request.session['image_code'] = {'code': code_str}
    # 设置session 60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

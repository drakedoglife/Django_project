#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 23:22
# @Author  : Aries
# @File    : user.py
# @Description : userInfo视图函数

from django.shortcuts import render, redirect
from website import models
from website.utils.pagenation import Pagination
from website.utils.form import UserModelForm


# 用户管理
def user_list(request):
    """用户管理"""

    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    # python方法获取数据
    # item.get_xxx_display()可以自动读取从数据库读取choices
    # item.depart_id获取到的是数字，使用item.depart直接获取数字对应的对象
    # for item in queryset:
    # print(item.id, item.name, item.account, item.onboarding_time.strftime("%Y-%m-%d"), item.get_gender_display())
    # print(item.name, item.depart.title)

    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    # 数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的那一行数据（对象），form = UserModelForm(instance=row_object)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的数据
        # 若想保存用户输入以外的值，只需 form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')

    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """删除用户"""
    obj = models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')

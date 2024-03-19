#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 23:22
# @Author  : Aries
# @File    : depart.py
# @Description : department视图函数

from django.shortcuts import render, redirect
from website import models
from website.utils.pagenation import Pagination


def depart_list(request):
    """部门列表"""

    # 去数据库获取部门列表
    queryset = models.Department.objects.all()

    page_object = Pagination(request=request, queryset=queryset, page_size=1)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, "depart_list.html", context)


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取用户post过来的数据
    title = request.POST['title']

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect('/depart/list')


def depart_delete(request, nid):
    """删除部门"""
    # 获取ID
    # http://127.0.0.1:8000/depart/delete/?nid=1
    # nid = request.GET.get('nid')
    # 第二种方法
    # http://127.0.0.1:8000/depart/1/edit
    # http://127.0.0.1:8000/depart/1/delete
    ##
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect('/depart/list/')


def depart_edit(request, nid):
    """修改部门"""
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    # 找到字段并更新 models.Department.objects.filter(id=nid).update(title=request.POST['title'], 其他=xxx)
    models.Department.objects.filter(id=nid).update(title=request.POST['title'])
    return redirect('/depart/list/')


def depart_index(request):
    return render(request, "index.html")

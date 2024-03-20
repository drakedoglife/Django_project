#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 23:22
# @Author  : Aries
# @File    : pretty.py
# @Description : prettyNum视图函数

from django.shortcuts import render, redirect, reverse
from website import models
from website.utils.pagenation import Pagination
from website.utils.form import PrettyModelForm, PrettyEditModelForm


# 靓号管理
def pretty_list(request):
    """获取靓号列表"""

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data is not None:
        data_dict['mobile__contains'] = search_data

    # 分页
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request=request, queryset=queryset)

    page_string = page_object.html()

    context = {
        'queryset': page_object.page_queryset,
        'search_data': search_data,
        'page_string': page_string,
        'total_page_count': page_object.total_page_count
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('pretty_list'))

    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    """编辑靓号"""
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(instance=row_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

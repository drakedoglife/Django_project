#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/20 11:28
# @Author  : Aries
# @File    : admin.py
# @Description : admin视图函数

from django.shortcuts import render, redirect, reverse
from website import models
from website.utils.pagenation import Pagination
from website.utils.form import AdminModelForm, AdminResetModelForm


def admin_list(request):
    """管理员账户"""

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data is not None:
        data_dict['username__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request=request, queryset=queryset, page_size=10)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('admin_list'))

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()

    if not row_object:
        return redirect(reverse('admin_list'))

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(instance=row_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('admin_list'))

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect(reverse('admin_list'))


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()

    if not row_object:
        return redirect(reverse('admin_list'))

    title = f"重置账户{row_object.username}的密码"

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect(reverse('admin_list'))

    return render(request, 'change.html', {'form': form, 'title': title})

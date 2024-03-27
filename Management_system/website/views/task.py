#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/24 14:48
# @Author  : Aries
# @File    : task.py
# @Description : ajax页面
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def task_list(request):
    return render(request, 'task_list.html')


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    # python 自带的json解析
    data_dict = request.POST
    # json_str = json.dumps(data_dict)
    # django自带的json解析
    return JsonResponse(data_dict)

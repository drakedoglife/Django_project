#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/26 11:18
# @Author  : Aries
# @File    : urls.py
# @Description : polls.url
from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

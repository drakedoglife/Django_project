"""
URL configuration for Management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from website.views import depart, pretty, user, admin, account, task

urlpatterns = [
    re_path(r'^$', account.login),
    # path("admin/", admin.site.urls),
    # 部门管理
    path("depart/list/", depart.depart_list, name='depart_list'),
    path("depart/add/", depart.depart_add, name='depart_add'),
    ##
    # http://127.0.0.1:8000/depart/1/edit
    # http://127.0.0.1:8000/depart/1/delete
    ##
    path("depart/<int:nid>/delete/", depart.depart_delete, name='depart_delete'),
    path("depart/<int:nid>/edit/", depart.depart_edit, name='depart_edit'),

    # 用户管理
    path("user/list/", user.user_list, name="user_list"),
    path("user/add/", user.user_add, name='user_add'),
    path("user/<int:nid>/edit/", user.user_edit, name="user_edit"),
    path("user/<int:nid>/delete/", user.user_delete, name="user_delete"),

    # 靓号管理
    path("pretty/list/", pretty.pretty_list, name="pretty_list"),
    path("pretty/add/", pretty.pretty_add, name="pretty_add"),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit, name="pretty_edit"),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete, name="pretty_delete"),

    # 管理员管理
    path("admin/list/", admin.admin_list, name="admin_list"),
    path("admin/add/", admin.admin_add, name="admin_add"),
    path("admin/<int:nid>/edit", admin.admin_edit, name="admin_edit"),
    path("admin/<int:nid>/delete", admin.admin_delete, name="admin_delete"),
    path("admin/<int:nid>/reset", admin.admin_reset, name="admin_reset"),

    # 登录
    path("login/", account.login, name="login"),
    path("logout/", account.logout, name='logout'),
    path("image/code/", account.image_code, name="image_code"),

    # ajax页面
    path("task/list/", task.task_list, name="task_list"),
    path("task/ajax/", task.task_ajax, name="task_ajax")
]

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
from django.urls import path
from website.views import depart, pretty, user

urlpatterns = [
    path("admin/", admin.site.urls),
    # 部门管理
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    ##
    # http://127.0.0.1:8000/depart/1/edit
    # http://127.0.0.1:8000/depart/1/delete
    ##
    path("depart/<int:nid>/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),
    path("", depart.depart_index),

    # 用户管理
    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/<int:nid>/edit/", user.user_edit, name="user_edit"),
    path("user/<int:nid>/delete/", user.user_delete, name="user_delete"),

    # 靓号管理
    path("pretty/list/", pretty.pretty_list, name="pretty_list"),
    path("pretty/add/", pretty.pretty_add, name="pretty_add"),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit, name="pretty_edit"),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete, name="pretty_delete"),
]

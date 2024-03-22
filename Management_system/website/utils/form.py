#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 22:40
# @Author  : 高一方
# @File    : form.py
# @Description : 这个文件用来存储form

from website import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from website.utils.bootstrap import BootstrapModelForm, BootstrapForm
from website.utils.encrypt import md5


# ModelForm实例
class UserModelForm(BootstrapModelForm):
    # password = forms.CharField(widget=forms.PasswordInput, label='密码')
    # onboarding_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}), label="入职时间")

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'gender', 'account', 'depart', 'onboarding_time']
        # 插件控制生成组件的属性
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
        #     'age': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        #     'account': forms.TextInput(attrs={'class': 'form-control'}),
        #     'gender': forms.Select(attrs={'class': 'form-control'}),
        #     'depart': forms.Select(attrs={'class': 'form-control'}),
        #     'onboarding_time': forms.DateTimeInput(attrs={'class': 'form-control'})
        # }


class PrettyModelForm(BootstrapModelForm):
    # 手机号正则校验，方法一
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[34578]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        # 直接添加所有字段
        fields = "__all__"
        # 排除某个字段
        # exclude = ["level"]

    # 手机号校验，方式二,钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exits = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exits:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 验证通过后返回
        return txt_mobile


# 在定义一个modelForm
class PrettyEditModelForm(BootstrapModelForm):
    # 手机号正则校验，方法一
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[34578]\d{9}$', '手机号格式错误')],
        disabled=False
    )

    class Meta:
        model = models.PrettyNum
        # 手机号无法修改
        fields = ['mobile', 'price', 'level', 'status']
        # 直接添加所有字段
        # fields = "__all__"
        # 排除某个字段
        # exclude = ["level"]

    # 手机号校验，方式二,钩子方法（排除自己以外是否重复）
    def clean_mobile(self):
        # 当前编辑那一行的id
        # self.instance.pk

        txt_mobile = self.cleaned_data['mobile']
        # （排除自己以外是否重复）
        exits = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.id).exists()

        if exits:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 验证通过后返回
        return txt_mobile


class AdminModelForm(BootstrapModelForm):
    """adminModelForm"""
    confirm_password = forms.CharField(max_length=64, label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        # MD5加密
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = md5(self.cleaned_data['confirm_password'])
        if password != confirm_password:
            raise ValidationError("两次密码输入不一致")

        # 返回什么，什么就保存到数据库
        return confirm_password


def is_password_valid(nid, password) -> bool:
    md5_password = md5(password)
    return models.Admin.objects.filter(id=nid, password=md5_password).exists()


class AdminResetModelForm(AdminModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminResetModelForm, self).__init__(*args, **kwargs)
        self.password = 0

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data['password']

        self.password = password
        # 去数据库校验新密码和当前密码是否一致
        if is_password_valid(nid=self.instance.pk, password=password):
            raise ValidationError("新密码不能与当前密码相同")

        return md5(password)

    def clean_confirm_password(self):
        if is_password_valid(nid=self.instance.pk, password=self.password):
            raise ValidationError("新密码不能与当前密码相同")
        else:
            password = self.cleaned_data['password']
            confirm_password = md5(self.cleaned_data['confirm_password'])

            if password != confirm_password:
                raise ValidationError("两次密码输入不一致")

            # 返回什么，什么就保存到数据库
            return confirm_password


class LoginForm(BootstrapForm):
    """loginform"""
    username = forms.CharField(required=True, max_length=32, widget=forms.TextInput(attrs={'class': "form-control"}),
                               label="用户名")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}), label="密码")

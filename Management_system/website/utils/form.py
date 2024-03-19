#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 22:40
# @Author  : 高一方
# @File    : form.py
# @Description : 这个文件用来存储form

sfrom website import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from website.utils.bootstrapform import BootstrapForm


# ModelForm实例
class UserModelForm(BootstrapForm):
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


class PrettyModelForm(BootstrapForm):
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
class PrettyEditModelForm(BootstrapForm):
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

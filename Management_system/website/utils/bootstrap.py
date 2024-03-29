#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/19 20:18
# @Author  : 我的名字
# @File    : bootstrap.py
# @Description : 这个函数是用来快速生成ModelForm的

from django import forms


class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }


class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass


class BootstrapForm(Bootstrap, forms.Form):
    pass

from django.shortcuts import render, redirect
from website import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from website.utils.pagenation import Pagination
from website.utils.bootstrapform import BootstrapForm


# Create your views here.
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


# 用户管理
def user_list(request):
    """用户管理"""

    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    # python方法获取数据
    # item.get_xxx_display()可以自动读取从数据库读取choices
    # item.depart_id获取到的是数字，使用item.depart直接获取数字对应的对象
    # for item in queryset:
    # print(item.id, item.name, item.account, item.onboarding_time.strftime("%Y-%m-%d"), item.get_gender_display())
    # print(item.name, item.depart.title)

    return render(request, 'user_list.html', context)


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


def user_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    # 数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的那一行数据（对象），form = UserModelForm(instance=row_object)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的数据
        # 若想保存用户输入以外的值，只需 form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')

    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """删除用户"""
    obj = models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


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


def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_add.html', {'form': form})


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

from django.shortcuts import render, HttpResponse, redirect
import requests


# Create your views here.
def index(request):
    return HttpResponse("欢迎使用")


def user_list(request):
    # 去app目录下的templates目录寻找目标html文件，根据app的注册顺序逐一查找他们的templates
    return render(request, "user_list.html")


def user_add(request):
    return render(request, "user_add.html")


def tpl(request):
    name = "gyf"
    roles = ["管理员", "CEO", "保安"]
    user_info = {"name": "gyf", "salary": 100000, "role": "CTO"}
    data_list = [
        {"name": "Tom", "salary": 12, "role": "a"},
        {"name": "Aries", "salary": 13, "role": "b"},
        {"name": "Darcy", "salary": 14, "role": "c"},
    ]
    data = {"n1": name, "n2": roles, "n3": user_info, "n4": data_list}
    return render(request, "tpl.html", data)


def something(request):
    # request是一个对象，封装了用户通过浏览器发送过来的所有数据
    print(request.method)  # GET POST
    # 在url上传递一些值
    print(request.GET)
    # 再请球体中提交数据
    print(request.POST)

    ## 响应
    # HttpResponse("返回内容")，内容字符串返回给请求者
    # return HttpResponse("返回内容")

    # 读取html内容
    # return render(request, "something.html", {"title": "来了"})

    #
    return redirect("https://www.baidu.com")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # 获取提交的数据
        print(request.POST)
        response = request.POST
        username = response.get("user")
        password = response.get("pwd")
        print(f"name is {username}, password is {password}")
        return HttpResponse("登录成功")

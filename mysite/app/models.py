from django.db import models


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()


class Department(models.Model):
    title = models.CharField(max_length=16)


# # # 新建数据 本质insert into app_department(title)values("销售部")
# Department.objects.create(title="销售部")

# UserInfo.objects.create(name='gyf')

# # # 删除数据
# UserInfo.objects.filter(id=2).delete();
# UserInfo.objects.all().delete();

# # 获取数据
# ## data_list = [row, row, row] QuerySet类型
# data_list = UserInfo.objects.all()
# for obj in data_list:
#     print(obj.id, obj.name, obj.age)

# # data_list2 = [row, ]
# data_list2 = UserInfo.objects.filter(id=1)

# # data_list3 = obj当只有一条数据时
# data_list3 = UserInfo.objects.filter(id=1).first()
# print(data_list3.id, data_list3.name, data_list3.age)

# ## 更新数据
# UserInfo.objects.all().update(password=999)
# UserInfo.objects.filter(id=2).update(password=999, name='gyf')

"""
create table app_userinfo(
    id bigint auto_increment primary key,  ## Django自动生成
    name varchar(32),
    password varchar(64),
    age int
)
"""

from django.db import models


# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""

    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    """
    max_digits=10 总共的数字长度为10
    decimal_places=2 小数位为2
    """
    account = models.DecimalField(
        verbose_name="账户余额", max_digits=10, decimal_places=2, default=0
    )
    onboarding_time = models.DateField(verbose_name="入职时间")

    # 这样写无约束不可取
    # depart_id = models.BigAutoField(verbose_name="部门ID")

    """
    有约束
    -to, 与哪张表关联; -to_field与表中哪一列数据关联
    Django自动
     - 写的depart
     - 生成数据列 depart_id
    若关联的表中有数据被删除了，两种处理办法
    1. depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE) 当前表对应的内容也跟着删除
    2. depart = models.ForeignKey(
        to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL
    ) 当前表对应的内容置空
    """
    depart = models.ForeignKey(verbose_name="部门",
                               to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL
                               )

    """
    添加性别列：在DJango中用代码约束内容只有男或女
    """
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    mobile = models.CharField(max_length=11, verbose_name="手机号")

    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级'),
    )
    level = models.SmallIntegerField(choices=level_choices, verbose_name="级别", default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态", default=2)

from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名', db_index=True)  # db_index=True 索引
    email = models.EmailField(max_length=32, verbose_name='邮箱')
    password = models.CharField(max_length=32, verbose_name='密码')
    mobile_phone = models.CharField(max_length=32, verbose_name='电话号')


class PricePolicy(models.Model):
    """ 价格策略表 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )

    category = models.SmallIntegerField(default=2, choices=category_choices, verbose_name='收费类型')
    title = models.CharField(max_length=32, verbose_name='标题')
    price = models.PositiveIntegerField(verbose_name='价格')  # 正整数

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间数')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小')

    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Transaction(models.Model):
    """交易记录"""
    status_choice = (
        (1, '未支付'),
        (2, '已支付'),
    )
    status = models.SmallIntegerField(choices=status_choice, verbose_name='交易状态')
    order = models.CharField(max_length=64, unique=True, verbose_name='订单号')  # 唯一索引

    user = models.ForeignKey(to='UserInfo', verbose_name='用户', on_delete=models.CASCADE)
    price_policy = models.ForeignKey(to='PricePolicy', verbose_name='价格策略', on_delete=models.CASCADE)

    count = models.IntegerField(help_text='0表示无限期', verbose_name='数量(年)')

    price = models.IntegerField(verbose_name='实际支付的价格')

    start_datetime = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_datetime = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Project(models.Model):
    """ 项目表 """
    COLOR_CHOICES = (
        (1, "#56b8eb"),  # 56b8eb
        (2, "#f28033"),  # f28033
        (3, "#ebc656"),  # ebc656
        (4, "#a2d148"),  # a2d148
        (5, "#20BFA4"),  # #20BFA4
        (6, "#7461c2"),  # 7461c2,
        (7, "#20bfa3"),  # 20bfa3,
    )

    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)

    use_space = models.BigIntegerField(verbose_name='项目已使用空间', default=0, help_text='字节')

    star = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    bucket = models.CharField(verbose_name='cos桶', max_length=128)
    region = models.CharField(verbose_name='cos区域', max_length=32)

    # 查询：可以省事；
    # 增加、删除、修改：无法完成
    # project_user = models.ManyToManyField(to='UserInfo',through="ProjectUser",through_fields=('project','user'))


class ProjectUser(models.Model):
    """ 项目参与者 """
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='参与者', to='UserInfo', on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)


from django.db import models


class Admin(models.Model):
    """ 管理员表 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='部门ID')

    # 1.有约束
    # - to 与那张表关联
    # - to_field 与表中的那一列关联
    # 2.django自动
    # - 写的depart
    # - 生成数据列 depart_id
    # 3.部门表被删除
    # 3.1级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)

    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0)

    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "未售卖"),
        (2, "已售卖"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细详细")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单表 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品名", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to=Admin, on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="图像", max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    # 本质上数据库也是CharField，自动保存数据。
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')


class KqTask(models.Model):
    """ kq任务 """
    item_number = models.CharField(verbose_name="项目编号", max_length=32)
    item_name = models.CharField(verbose_name="项目名称", max_length=64)
    task_number = models.CharField(verbose_name="任务编号", max_length=32)
    task_name = models.CharField(verbose_name="任务名称", max_length=64)
    report_task_num = models.CharField(verbose_name="项目编号", max_length=32)
    task_proportion = models.FloatField(verbose_name="任务占比")
    reporter_depart = models.CharField(verbose_name="汇报人部门", max_length=64)
    reporter_number = models.CharField(verbose_name="汇报人编号", max_length=32)
    reporter_name = models.CharField(verbose_name="汇报人姓名", max_length=32)
    report_date = models.DateField(verbose_name="汇报日期")
    report_task_date = models.DateField(verbose_name="报工日期")
    work_detail = models.TextField(verbose_name="工作内容")
    workload = models.CharField(verbose_name="当日投入工作量", max_length=32)
    auditor_number = models.CharField(verbose_name="审核人编号", max_length=32)
    auditor = models.CharField(verbose_name="审核人", max_length=32)
    audit_completion_rate = models.CharField(verbose_name="审核完成率", max_length=32)
    audit_result = models.CharField(verbose_name="审核结果", max_length=32)
    get_your_work_done_today = models.CharField(verbose_name="今日完成工作量", max_length=32)
    way_to_report_work = models.CharField(verbose_name="报工方式", max_length=32)
    item_big_type = models.CharField(verbose_name="项目大类", max_length=32)
    item_type = models.CharField(verbose_name="项目类型", max_length=32)
    task_leader_no = models.CharField(verbose_name="任务负责人编号", max_length=32)
    task_auditor_no = models.CharField(verbose_name="任务审核人编号", max_length=32)


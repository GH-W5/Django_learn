# -*- coding:UTF-8 -*-

# datetime:2022/6/15 13:06
# software: PyCharm
"""
//
//                       .::::.
//                     .::::::::.
//                    :::::::::::
//                 ..:::::::::::'
//              '::::::::::::'
//                .::::::::::
//           '::::::::::::::..
//                ..::::::::::::.
//              ``::::::::::::::::
//               ::::``:::::::::'        .:::.
//              ::::'   ':::::'       .::::::::.
//            .::::'      ::::     .:::::::'::::.
//           .:::'       :::::  .:::::::::' ':::::.
//          .::'        :::::.:::::::::'      ':::::.
//         .::'         ::::::::::::::'         ``::::.
//     ...:::           ::::::::::::'              ``::.
//    ```` ':.          ':::::::::'                  ::::..
//                       '.:::::'                    ':'````..
"""
"""
文件说明：
    
"""
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]


class NumModelForm(BootStrapModelForm):
    # 验证：方式1    字段+正则
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]

    # 验证：方式2    钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        if models.PrettyNum.objects.filter(mobile=txt_mobile).exists():
            raise ValidationError("手机号已存在")

        # if len(txt_mobile) != 11:
        #     # 验证不通过
        #     raise ValidationError("格式错误")

        # 验证通过，用户输入的值返回
        return txt_mobile


class NumEditModelForm(BootStrapModelForm):
    # 验证：方式1    字段+正则
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]

    # 验证：方式2    钩子方法
    def clean_mobile(self):
        # 当前编辑的id
        # self.instance.pk

        txt_mobile = self.cleaned_data["mobile"]

        if models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists():
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 钩子方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm = md5(self.cleaned_data["confirm_password"])
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # 返回什么，以后保存到数据就是什么
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 钩子方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm = md5(self.cleaned_data["confirm_password"])
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # 返回什么，以后保存到数据就是什么
        return confirm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)


class TaskModeForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = []
        exclude= ["oid", "admin"]


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ["img"]

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="图像")


class UpModalForm(BootStrapModelForm):
    bootstrap_exclude_fields = ["img"]
    class Meta:
        model = models.City
        fields = "__all__"


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
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


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
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm

import random
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def depart_list(request):
    """ 部门列表 """

    # 去数据库获取所有的部门信息
    # [obj, obj]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """

    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据
    title = request.POST.get('title')

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回到部门列表
    return redirect('/depart/list/')


def depart_delete(request):
    """ 删除部门 """
    # 获取id
    # http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect('/depart/list')


# http://127.0.0.1:8000/depart/1/edit/
def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        # 根据nid，获取它的数据 【obj】
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get('title')
    # 根据ID找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)
    # 重定向回到部门列表
    return redirect('/depart/list/')


def user_list(request):
    """ 用户列表 """
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset=queryset)
    context = {
        'queryset': page_object.page_queryset,  # 分完页数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户 """

    if request.method == 'GET':
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)

    # 获取用户POST提交过来的数据
    name = request.POST.get("name")

    # 保存到数据库
    models.UserInfo.objects.create(name=name)

    # 重定向回到部门列表
    return redirect('/user/list/')


# ##############################ModelForm实例#######################################


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]


def user_model_form_add(request):
    """ 添加用户 ModelForm版本 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    # 校验失败 （在页面上显示错误信息）
    return render(request, "user_model_form_add.html", {"form": form})


def user_delete(request, nid):
    """ 删除用户 """
    # 删除
    models.UserInfo.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect('/user/list')


def user_edit(request, nid):
    """ 编辑用户 """
    # 根据nid，获取它的数据 【obj】
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    # 校验失败 （在页面上显示错误信息）
    return render(request, "user_model_form_add.html", {"form": form})


# ################################# 靓号管理 ##########################
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


def num_list(request):
    """ 靓号列表 """
    # for i in range(1500):
    #     mobile = str(int(random.uniform(13, 20)*10e8))
    #     models.PrettyNum.objects.create(mobile=mobile, price=i*500, level=i%4+1, status=i%2+1)

    # 查找靓号
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict = {"mobile__contains": search_data}

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request, queryset=queryset)

    context = {
        "search_data": search_data,

        'queryset': page_object.page_queryset,  # 分完页数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'num_list.html', context)


def num_model_form_add(request):
    """ 添加用户 ModelForm版本 """
    if request.method == "GET":
        form = NumModelForm()
        return render(request, "num_model_form_add.html", {"form": form})

    # 用户POST提交数据，数据校验
    form = NumModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/num/list/")
    # 校验失败 （在页面上显示错误信息）
    return render(request, "num_model_form_add.html", {"form": form})


def num_delete(request, nid):
    """ 删除用户 """
    # 删除
    models.PrettyNum.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect('/num/list')


def num_edit(request, nid):
    """ 编辑用户 """
    # 根据nid，获取它的数据 【obj】
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumEditModelForm(instance=row_object)
        return render(request, 'num_edit.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = NumEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/num/list/")
    # 校验失败 （在页面上显示错误信息）
    return render(request, "num_model_form_add.html", {"form": form})

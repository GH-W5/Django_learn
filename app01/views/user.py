# -*- coding:UTF-8 -*-

# datetime:2022/6/15 13:12
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
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


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

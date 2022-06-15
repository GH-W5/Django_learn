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
from app01.utils.form import NumEditModelForm, NumModelForm


# ################################# 靓号管理 ##########################
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
    return render(request, "num_edit.html", {"form": form})

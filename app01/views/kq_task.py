# -*- coding:UTF-8 -*-

# datetime:2022/6/17 9:45
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
import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import KqTaskModelForm
from app01.utils.pagination import Pagination


def task_list(request):
    """ 订单列表 """
    # 去数据库获取所有的订单
    queryset = models.KqTask.objects.all().order_by('-id')

    page_object = Pagination(request, queryset)

    form = KqTaskModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "kq_task_list.html", context)


@csrf_exempt
def task_add(request):
    """ 新建订单 （Ajax请求） """
    # 1.用户发送过来的数据进行校验   （ModelForm 进行校验）
    form = KqTaskModelForm(data=request.POST)
    if form.is_valid():
        # 额外添加一些不是用户输入的值（机子计算出来）
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 固定设置管理员ID
        form.instance.admin_id = request.session["info"]["id"]

        # 保存到数据库
        form.save()
        data_dict = {"status": True}
        # return HttpResponse(json.dumps(data_dict))
        return JsonResponse(data_dict)

    data_dict = {"status": False, 'error': form.errors}
    # return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    return JsonResponse(data_dict)


def task_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    exists = models.KqTask.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "数据不存在，删除失败。"})
    models.KqTask.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def task_ditail(request):
    """ 根据ID获取订单详细 """
    # 方式一
    """ 
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "error": "数据不存在，编辑失败。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        },
    }
    return JsonResponse(result)
    """

    # 方式二
    uid = request.GET.get("uid")
    row_dict = models.KqTask.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在，编辑失败。"})

    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def task_edit(request):
    """ 编辑订单 （Ajax请求） """
    uid = request.GET.get("uid")
    row_object = models.KqTask.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在。"})
    form = KqTaskModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})

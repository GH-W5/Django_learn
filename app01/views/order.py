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
from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination


def order_list(request):
    """ 订单列表 """
    # 去数据库获取所有的订单
    queryset = models.Order.objects.all().order_by('-id')

    page_object = Pagination(request, queryset)

    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """ 新建订单 （Ajax请求） """
    # 1.用户发送过来的数据进行校验   （ModelForm 进行校验）
    form = OrderModelForm(data=request.POST)
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


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    exists =  models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "数据不存在，删除失败。"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})
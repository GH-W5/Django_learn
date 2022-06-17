# -*- coding:UTF-8 -*-

# datetime:2022/6/16 22:03
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
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import TaskModeForm
from app01.utils.pagination import Pagination


def task_list(request):
    """" 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')

    page_object = Pagination(request, queryset)

    form = TaskModeForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    # print(request.GET)
    print("后台获取提交数据：", request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    print("后台获取提交数据：", request.POST)

    # 1.用户发送过来的数据进行校验   （ModelForm 进行校验）
    form = TaskModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

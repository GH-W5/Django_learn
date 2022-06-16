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


def task_list(request):
    """" 任务列表 """
    return render(request, "task_list.html")


@csrf_exempt
def task_ajax(request):
    # print(request.GET)
    print("后台获取提交数据：", request.POST)
    data_dict = {"status": True, "data":[11,22,33,44]}
    return HttpResponse(json.dumps(data_dict))

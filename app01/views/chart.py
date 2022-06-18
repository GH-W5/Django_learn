# -*- coding:UTF-8 -*-

# datetime:2022/6/18 16:17
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
from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart_list.html")


def chart_bar(request):
    """ 构造柱状图数据 """
    # 可以去数据库获取
    legend = ["量济宁", "吴佩琪"]
    series_list = [
        {
            "name": '量济宁',
            "type": 'bar',
            "data": [5, 20, 36, 10, 5, 20]
        },
        {
            "name": '吴佩琪',
            "type": 'bar',
            "data": [15, 66, 32, 22, 44, 55]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }

    }
    return JsonResponse(result)

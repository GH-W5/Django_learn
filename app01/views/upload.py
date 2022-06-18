# -*- coding:UTF-8 -*-

# datetime:2022/6/18 19:38
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
from django.shortcuts import render, HttpResponse


def upload_list(request):
    """ 上传文件 """
    if request.method == "GET":
        return render(request, "upload_list.html")
    # print(request.POST)     # 请求体中的数据
    # print(request.FILES)    # 请求发过来的文件
    file_object = request.FILES.get("avatar")
    # print(file_object.name)

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("....")

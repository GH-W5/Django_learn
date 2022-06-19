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
import os
from django.shortcuts import render, HttpResponse

from app01.utils.form import UpForm
from app01 import models


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


def upload_form(request):
    """ 上传文件 """
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        context = {
            "form": form,
            "title": title,
        }
        return render(request, "upload_form.html", context)

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1.读取图片内容。写入到文件夹中并获取文件路径
        image_object = form.cleaned_data.get("img")
        db_file_path = os.path.join("static", "img", image_object.name)
        file_path = os.path.join("app01", db_file_path)
        f = open(file_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2.将图片文件路径写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_file_path,
        )
        return HttpResponse("....")

    return render(request, "upload_form.html", {"form": form, "title": title, })

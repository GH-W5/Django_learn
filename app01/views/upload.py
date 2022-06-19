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
from django.conf import settings

from app01.utils.form import UpForm, UpModalForm
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

        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)

        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2.将图片文件路径写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )
        return HttpResponse("....")

    return render(request, "upload_form.html", {"form": form, "title": title, })


def upload_modal_form(request):
    """ 基于modalform上传文件和数据 """
    if request.method == "GET":
        form = UpModalForm
        return render(request, "upload_form.html", {"form": form, "title": "ModalForm上传文件"})

    form = UpModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 自动保存到数据库
        form.save()
        return HttpResponse("上传成功")
    return render(request, "upload_form.html", {"form": form, "title": "ModalForm上传文件"})
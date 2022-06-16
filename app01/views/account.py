# -*- coding:UTF-8 -*-

# datetime:2022/6/16 3:00
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
from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import LoginForm


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # print(form.cleaned_data)

        # 去数据库校验用户名和密码是否正确，获取用户名对象，None
        # models.Admin.objects.filter(username='',password='').first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        # 用户名和密码正确
        # 网站生成一个随机字符串；写到用户浏览器的cookie中；再写入到session中；
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")

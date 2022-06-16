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
from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import LoginForm
from app01.utils.code import check_code


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # print(form.cleaned_data)

        # 取出用户输入验证码
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        # 判断验证码
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # 去数据库校验用户名和密码是否正确，获取用户名对象，None
        # models.Admin.objects.filter(username='',password='').first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        # 用户名和密码正确
        # 网站生成一个随机字符串；写到用户浏览器的cookie中；再写入到session中；
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        # 用户信息session可以保存1小时
        request.session.set_expiry(60*60)

        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})


def image_code(request):
    """ 生成图片验证码 """
    # 调用pillow，生成图片
    img, code_string = check_code()

    # 字符串写入到自己的session，以便后期获取，校验
    request.session["image_code"] = code_string
    # 给session设置60s后超时
    request.session.set_expiry(60)

    # 写入内存(Python3)
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")

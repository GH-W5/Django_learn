# -*- coding:UTF-8 -*-

# datetime:2022/6/16 8:20
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
文件说明：中间件
    
"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 没有返回值，默认返回None，继续往后走
        # 如果有返回值 HttpResponse、render、redirect
        print("M1.process_request")

    def process_response(self, request, response):
        print("M1.process_response")
        return response


class AuthMiddleware(MiddlewareMixin):
    """ 登录验证中间件 """

    def process_request(self, request):
        # 0. 排除不需要登录就能访问的页面
        # request.path_info：获取当前用户请求的url  /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，能读到则用户已登录过，继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.没有登陆过，回到登陆页面
        return redirect("/login/")

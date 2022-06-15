# -*- coding:UTF-8 -*-

# datetime:2022/6/15 8:08
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
文件说明：自定义的分页组件
    
"""
import copy
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(
            self,
            request,
            queryset,
            page_size=10,
            page_param="page",
            plus=5,
    ):
        """

        :param request: 请求对象
        :param queryset: 查询符合条件的数据（根据这个数据对它进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中获取分页的参数 例如：num/list/?page=7
        :param plus: 根据当前页显示前\后几页
        """
        self.page_size = page_size
        self.page_param = page_param
        self.plus = plus

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        # 根据用户想要访问的页码，计算出起止位置
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        # 数据总条数
        total_count = queryset.count()
        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    def html(self):
        # 计算出当前页的前5页和后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多，大于11页
            # 当前页小于5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页大于5
                # 当前页+5大于总页码
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码 由后台计算并加入到前端中
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < end_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 页码搜索框
        search_string = """
                <li>
                    <form style="float: left;margin-left: -1px;" method="get">
                        <input type="text" name="page" class="form-control" placeholder="页码"
                        style="position:relative;float:left;display:inline-block;width: 80px;border-radius:0;" >
                        <button style="border-radius: 0;" class="btn btn-default" type="submit">跳转</button>
                    </form>
                </li>
            """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string

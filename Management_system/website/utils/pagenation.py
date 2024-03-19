"""
自定义分页组件
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    """
    这个类实现了分页功能
    """
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start_page = (page - 1) * page_size
        self.end_page = page * page_size

        self.page_queryset = queryset[self.start_page: self.end_page]

        self.total_count = queryset.count()
        total_page_count, div = divmod(self.total_count, self.page_size)

        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

        self.page_param = page_param

    def html(self):
        # 根据当前页计算出前五页和后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库数据比较少，没有达到11页
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 数据库数据比较多
            # 当前页小于5（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页数大于5
                # 如果当前页+5大于总页码
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])

        # 首页
        first_page = f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>'
        page_str_list.append(first_page)

        # 上一页
        if self.page == 1:
            self.query_dict.setlist(self.page_param, [self.page])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)

        # 下一页
        if self.page == self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next_page = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        page_str_list.append(next_page)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last_page = f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>'
        page_str_list.append(last_page)

        # 搜索
        search_string = """
            <li>
                            <form method="get" style="width: 300px; float: left; margin-left: 10px">
                                <div class="input-group">
                                    <input type="number" class="form-control" placeholder="输入页码" name="page">
                                    <span class="input-group-btn"><button class="btn btn-default"
                                                                          type="submit">跳转至</button></span>
                                </div>
                            </form>
                        </li>
            """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string

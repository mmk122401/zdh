from django.http.request import QueryDict


class Pagination():

    def __init__(self, page_num, all_count, params=None, per_num=10, max_show=11):
        '''

        :param page_num:        当前页码数
        :param all_count:       总数据量
        :param per_num:         每页显示的数据条数
        :param max_show:        最大显示页码数
        :param total_page_num:  总页码数
        :param page_start:      起始页码数
        :param page_end:        终止页码数
        :param params:          地址
        '''
        try:
            page_num = int(page_num)  # page是地址上自己起的名字
            if page_num <= 0:
                page_num = 1
        except Exception as e:
            page_num = 1
        self.params = params if params else QueryDict(mutable=True)
        self.page_num = page_num
        self.per_num = per_num  # 每页显示的数据
        self.all_count = all_count  # 总数据量
        # 总页码数
        total_page_num, more = divmod(all_count, per_num)  # divmod(all_count,per_num) 这是一个方法，第一个表示除数，第二个是被除数
        if more:  # 如果有余数，页码加一
            total_page_num += 1
        half_show = max_show // 2
        # 总页码数不足以满足最大页码数
        if total_page_num < max_show:
            page_start = 1
            page_end = total_page_num
        else:
            if page_num - half_show <= 0:
                page_start = 1
                page_end = max_show
            elif page_num + half_show > total_page_num:
                page_start = total_page_num - max_show + 1
                page_end = total_page_num
            else:
                # 页码起始值
                page_start = page_num - half_show
                # 页码终止值
                page_end = page_num + half_show
        self.page_start = page_start
        self.page_end = page_end
        self.total_page_num = total_page_num

    @property
    def page_html(self):
        page_list = []
        # 上一页
        if self.page_num == 1:
            page_list.append('<li class="disabled"><a><span>&laquo;</span></a></li>')
        else:
            # query=alex page=2
            self.params['page'] = self.page_num - 1
            page_list.append('<li><a href="?{}"><span>&laquo;</span></a></li>'.format(self.params.urlencode()))

        for i in range(self.page_start, self.page_end + 1):  # 循环生成页码
            self.params['page'] = i
            if i == self.page_num:
                page_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
        # 下一页
        if self.page_num == self.total_page_num:
            page_list.append('<li class="disabled"><a><span>&raquo;</span></a></li>')
        else:
            self.params['page'] = self.page_num + 1
            page_list.append('<li><a href="?{}"><span>&raquo;</span></a></li>'.format(self.params.urlencode()))
        return ''.join(page_list)  # 拼接

    @property
    def start(self):
        return (self.page_num - 1) * self.per_num  # 开始页

    @property
    def end(self):
        return self.page_num * self.per_num  # 结束页

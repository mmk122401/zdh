from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
import hashlib
from crm.forms import RegForm, CustomerForm, ConsultForm, EnrollmentForm, ClassListForm, CourseRecordForm, \
    StudyRecordForm
from django.views import View
from django.db.models import Q
from utils.pagination import Pagination
from django.forms import modelformset_factory


# Create your views here.
# 登录
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode('utf8'))
        password = md5.hexdigest()
        obj = models.UserProfile.objects.filter(username=username, password=password, is_active=True).first()
        if obj:
            # 登录成功 跳转到首页
            # 保存当前用户的ID
            request.session['pk'] = obj.pk
            return redirect('index')
        return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


# 注册
def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('login')
        print(form_obj.cleaned_data)
    return render(request, 'reg.html', {'form_obj': form_obj})


# 客户表
def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        all_customer = models.Customer.objects.filter(consultant=request.user_obj)  # 通过自定义中间件获取用户的销售
    return render(request, 'customer_list.html', {'all_customer': all_customer})


class CustomerList(View):
    def get(self, request, *args, **kwargs):
        q = self.search(['qq', 'name', 'consultant__name'])
        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.user_obj)  # 通过自定义中间件获取用户的销售

        page = Pagination(request.GET.get('page', '1'), all_customer.count(), request.GET.copy(),
                          2)  # request.GET 拿到的是一个Queryset字典对象，需要深拷贝才能进行修改
        return render(request, 'customer_list.html',
                      {'all_customer': all_customer[page.start:page.end], 'page_html': page.page_html})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if hasattr(self, action):  # 通过反射去调select中的option对应的value值，传到浏览器是字符串，用反射
            getattr(self, action)()
        else:
            return HttpResponse('别搞事儿！')
        return self.get(request, *args, **kwargs)

    def muti_apply(self):
        # 公户变私户
        # 获取所选的项
        ids = self.request.POST.getlist('ids')  # 拿到的是列表
        models.Customer.objects.filter(pk__in=ids).update(consultant=self.request.user_obj)

    def muti_pub(self):
        # 私户变公户
        ids = self.request.POST.getlist('ids')
        models.Customer.objects.filter(pk__in=ids).update(consultant=None)

    # 自定义一个search方法，用来模糊查询
    def search(self, field_list):
        query = self.request.GET.get('query', '')  # 拿到搜索框中的值
        q = Q()  # 实例化Q对象
        q.connector = 'OR'  # 把q的关系改成or，默认是and
        for field_name in field_list:
            q.children.append(Q(('{}__contains'.format(field_name), query)))
        return q


# 增加客户
def add_customer(request):
    form_obj = CustomerForm()
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'add_customer.html', {'form_obj': form_obj})


# 删除客户
def del_customer(request, pk):
    models.Customer.objects.filter(pk=pk).delete()
    return redirect(reverse('customer_list'))


# 编辑客户
def edit_customer(request, pk):
    data = models.Customer.objects.filter(pk=pk).first()
    form_obj = CustomerForm(instance=data)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=data)
        form_obj.save()
        return redirect(reverse('customer_list'))
    return render(request, 'edit_customer.html', {'form_obj': form_obj})


# 跟进记录展示
class ConsultList(View):
    def get(self, request, customer_id=None, *args, **kwargs):
        q = self.search(['status', 'customer__name'])
        if not customer_id:
            all_consult = models.ConsultRecord.objects.filter(q, consultant=request.user_obj,
                                                              delete_status=False).order_by('-date')  # 通过自定义中间件获取用户的销售
        else:
            all_consult = models.ConsultRecord.objects.filter(q, customer_id=customer_id, delete_status=False).order_by(
                '-date')
        page = Pagination(request.GET.get('page', '1'), all_consult.count(), request.GET.copy(),
                          2)  # request.GET 拿到的是一个Queryset字典对象，需要深拷贝才能进行修改
        return render(request, 'consult_list.html',
                      {'all_consult': all_consult[page.start:page.end], 'page_html': page.page_html})

    # 自定义一个search方法，用来模糊查询
    def search(self, field_list):
        query = self.request.GET.get('query', '')  # 拿到搜索框中的值
        q = Q()  # 实例化Q对象
        q.connector = 'OR'  # 把q的关系改成or，默认是and
        for field_name in field_list:
            q.children.append(Q(('{}__contains'.format(field_name), query)))
        return q


# 添加跟进记录
def add_consult(request):
    obj = models.ConsultRecord(consultant=request.user_obj)
    form_obj = ConsultForm(instance=obj)
    title = '添加跟进记录'
    if request.method == "POST":
        form_obj = ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_list'))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


# 删除跟进
def del_consult(request, del_id):
    models.ConsultRecord.objects.filter(pk=del_id).delete()
    return redirect(reverse('consult_list'))


# 编辑跟进记录
def edit_consult(request, edit_id):
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
    form_obj = ConsultForm(instance=obj)
    title = '编辑跟进记录'
    if request.method == "POST":
        form_obj = ConsultForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_list'))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class EnrollmentList(View):
    def get(self, request, customer_id=None, *args, **kwargs):
        q = self.search([])
        # 当前销售的所有客户的报名表
        all_enrollment = models.Enrollment.objects.filter(q, delete_status=False,
                                                          customer__in=request.user_obj.customers.all())
        page = Pagination(request.GET.get('page', '1'), all_enrollment.count(), request.GET.copy(),
                          2)  # request.GET 拿到的是一个Queryset字典对象，需要深拷贝才能进行修改
        return render(request, 'enrollment_list.html',
                      {'all_enrollment': all_enrollment[page.start:page.end], 'page_html': page.page_html})

    # 自定义一个search方法，用来模糊查询
    def search(self, field_list):
        query = self.request.GET.get('query', '')  # 拿到搜索框中的值
        q = Q()  # 实例化Q对象
        q.connector = 'OR'  # 把q的关系改成or，默认是and
        for field_name in field_list:
            q.children.append(Q(('{}__contains'.format(field_name), query)))
        return q


def enrollment_change(request, customer_id=None, edit_id=None):
    obj = models.Enrollment(customer_id=customer_id) if customer_id else models.Enrollment.objects.filter(
        pk=edit_id).first()
    form_obj = EnrollmentForm(instance=obj)
    title = '添加报名表' if customer_id else '编辑报名表'
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            return redirect(next)
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class ClassList(View):
    def get(self, request, customer_id=None, *args, **kwargs):
        q = self.search([])
        all_class = models.ClassList.objects.filter(q)
        page = Pagination(request.GET.get('page', '1'), all_class.count(), request.GET.copy(),
                          2)  # request.GET 拿到的是一个Queryset字典对象，需要深拷贝才能进行修改
        return render(request, 'class_list.html',
                      {'all_class': all_class[page.start:page.end], 'page_html': page.page_html})

    # 自定义一个search方法，用来模糊查询
    def search(self, field_list):
        query = self.request.GET.get('query', '')  # 拿到搜索框中的值
        q = Q()  # 实例化Q对象
        q.connector = 'OR'  # 把q的关系改成or，默认是and
        for field_name in field_list:
            q.children.append(Q(('{}__contains'.format(field_name), query)))
        return q


def class_change(request, edit_id=None):
    obj = models.ClassList.objects.filter(pk=edit_id).first()
    form_obj = ClassListForm(instance=obj)
    title = '编辑班级' if edit_id else '添加班级'
    if request.method == 'POST':
        form_obj = ClassListForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            return redirect(next)
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


class BaseView(View):
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if hasattr(self, action):  # 通过反射去调select中的option对应的value值，传到浏览器是字符串，用反射
            getattr(self, action)()
        else:
            return HttpResponse('别搞事儿！')
        return self.get(request, *args, **kwargs)

    def search(self, field_list):
        query = self.request.GET.get('query', '')  # 拿到搜索框中的值
        q = Q()  # 实例化Q对象
        q.connector = 'OR'  # 把q的关系改成or，默认是and
        for field_name in field_list:
            q.children.append(Q(('{}__contains'.format(field_name), query)))
        return q


class CourseRecordList(BaseView):
    def get(self, request, *args, class_id, **kwargs):
        q = self.search([])
        all_course_record = models.CourseRecord.objects.filter(q, re_class_id=class_id)
        page = Pagination(request.GET.get('page', '1'), all_course_record.count(), request.GET.copy(),
                          2)  # request.GET 拿到的是一个Queryset字典对象，需要深拷贝才能进行修改
        return render(request, 'course_record_list.html',
                      {'all_course_record': all_course_record[page.start:page.end], 'page_html': page.page_html,
                       'class_id': class_id})

    def multi_init(self):
        # 批量初始化学习记录
        print(self.request.POST)
        course_record_ids = self.request.POST.get('ids', [])
        for course_record_id in course_record_ids:
            # 根据一个课程ID生成学习记录
            course_record_obj = models.CourseRecord.objects.filter(pk=course_record_id).first()
            # 找到当前班级的所有学生
            students = course_record_obj.re_class.customer_set.filter(status='studying')
            print(students)
            # for student in students:
            #     models.StudyRecord.objects.get_or_create(student=student,
            #                                              course_record_id=course_record_id)  # 有就拿，没有就创建

            # 批量插入
            study_record_list = []
            for student in students:
                if not models.StudyRecord.objects.filter(student=student, course_record_id=course_record_id).exists():
                    study_record_list.append(models.StudyRecord(student=student, course_record_id=course_record_id))
            models.StudyRecord.objects.bulk_create(study_record_list)


def course_record_change(request, class_id=None, edit_id=None):
    obj = models.CourseRecord(re_class_id=class_id, recorder=request.user_obj) \
        if class_id else models.CourseRecord.objects.filter(pk=edit_id).first()
    form_obj = CourseRecordForm(instance=obj)
    title = '添加课程记录' if class_id else '编辑课程记录'
    if request.method == 'POST':
        form_obj = CourseRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next')
            return redirect(next)
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})


def study_record_list(request, course_record_id=None):
    FormSet = modelformset_factory(models.StudyRecord, form=StudyRecordForm, extra=0)
    formset_obj = FormSet(queryset=models.StudyRecord.objects.filter(course_record_id=course_record_id))
    if request.method == 'POST':
        formset_obj = FormSet(data=request.POST)
        if formset_obj.is_valid():
            formset_obj.save()
    return render(request, 'study_record_list.html', {'formset_obj': formset_obj})

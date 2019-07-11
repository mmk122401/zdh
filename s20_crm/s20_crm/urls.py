"""s20_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from crm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^reg/$', views.reg, name='reg'),
    url(r'^index/$', views.index, name='index'),

    url(r'^customer_list/$', views.CustomerList.as_view(), name='customer_list'),
    url(r'^my_customer/$', views.CustomerList.as_view(), name='my_customer'),

    url(r'^add_customer/$', views.add_customer, name='add_customer'),
    url(r'^del_customer/(\d+)/$', views.del_customer, name='del_customer'),
    url(r'^edit_customer/(\d+)/$', views.edit_customer, name='edit_customer'),

    url(r'^consult_list/$', views.ConsultList.as_view(), name='consult_list'),  # 某个销售的所有客户的跟进记录
    url(r'^consult_list/(\d+)/$', views.ConsultList.as_view(), name='one_consult_list'),  # 某个客户的所有跟进记录
    url(r'^add_consult/$', views.add_consult, name='add_consult'),
    url(r'^edit_consult/(\d+)/$', views.edit_consult, name='edit_consult'),
    url(r'^del_consult/(\d+)/$', views.del_consult, name='del_consult'),

    url(r'^enrollment_list/$', views.EnrollmentList.as_view(), name='enrollment_list'),
    url(r'^add_enrollment/(?P<customer_id>\d+)$', views.enrollment_change, name='add_enrollment'),
    url(r'^edit_enrollment/(?P<edit_id>\d+)$', views.enrollment_change, name='edit_enrollment'),

    url(r'^class_list/$', views.ClassList.as_view(), name='class_list'),
    url(r'^add_class/$', views.class_change, name='add_class'),
    url(r'^edit_class/(?P<edit_id>\d+)$', views.class_change, name='edit_class'),

    # 展示某个班级的课程记录
    url(r'^course_record_list/(?P<class_id>\d+)$', views.CourseRecordList.as_view(), name='course_record_list'),
    url(r'^add_course_record/(?P<class_id>\d+)$', views.course_record_change, name='add_course_record'),
    url(r'^edit_course_record/(?P<edit_id>\d+)$', views.course_record_change, name='edit_course_record'),

    # 展示某个课程记录的学习记录
    url(r'^study_record_list/(?P<course_record_id>\d+)$', views.study_record_list, name='study_record_list'),
]

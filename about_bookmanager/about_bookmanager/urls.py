"""about_bookmanager URL Configuration

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
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),

    url(r'^book_list/', views.Booklist.as_view(), name='book_list'),
    url(r'^add_book/', views.AddBook.as_view(), name='add_book'),
    url(r'^del_book/(\d+)/', views.del_book, name='del_book'),
    url(r'^edit_book/(\d+)/', views.edit_book, name='edit_book'),
]

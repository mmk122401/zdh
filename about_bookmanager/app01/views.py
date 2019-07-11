from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
from app01 import models
import hashlib


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = models.User.objects.filter(name=username, password=password)
        if obj:
            return redirect(reverse('book_list'))
        return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        obj = models.User.objects.create(name=username, password=password, email=email)
        return redirect(reverse('login'))
    return render(request, 'register.html')


class Booklist(View):
    def get(self, request):
        book_obj = models.Book.objects.all()
        return render(request, 'booklist.html', {'book_obj': book_obj})


class AddBook(View):
    def get(self, request):
        return render(request, 'add_book.html')

    def post(self, request):
        book_name = request.POST.get('book_name')
        price = request.POST.get('price')
        date = request.POST.get('date')
        publisher = request.POST.get('publisher')
        ret = models.Book.objects.create(bookname=book_name, price=price, date=date, publisher=publisher)
        return redirect(reverse('book_list'))


def del_book(request, pk):
    models.Book.objects.filter(pk=pk).delete()
    return redirect(reverse('book_list'))


def edit_book(request, pk):
    edit_obj = models.Book.objects.get(pk=pk)
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        price = request.POST.get('price')
        date = request.POST.get('date')
        publisher = request.POST.get('publisher')
        edit_obj.bookname = book_name
        edit_obj.price = price
        edit_obj.date = date
        edit_obj.publisher = publisher
        edit_obj.save()
        return redirect(reverse('book_list'))
    books = models.Book.objects.all()
    return render(request, 'edit_book.html', {'edit_obj': edit_obj, 'books': books})

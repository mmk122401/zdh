from django.db import models


# Create your models here.

class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    bookname = models.CharField(max_length=32)
    price = models.IntegerField()
    date = models.DateField()
    publisher = models.CharField(max_length=32)


class User(models.Model):
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=255, unique=True, null=True)

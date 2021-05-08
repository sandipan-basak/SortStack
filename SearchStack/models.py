from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=15)

class Folder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=20, unique=True)

class Article(models.Model):
    title = models.CharField(max_length=500)
    view_count = models.IntegerField(blank=True, null=True)
    link = models.URLField(max_length=250, default='https://stackoverflow.com/')
    creation_date = models.DateTimeField(blank=True, null=True, default=date.fromtimestamp(0))

class ArticleList(models.Model):
    title = models.CharField(max_length=500)
    view_count = models.IntegerField(blank=True, null=True)
    link = models.URLField(max_length=250, default='https://stackoverflow.com/')
    creation_date = models.DateTimeField(blank=True, null=True, default=date.fromtimestamp(0))


from django.contrib import admin

from .models import User, Article, Folder, ArticleList

# Register your models here.
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Folder)
admin.site.register(ArticleList)

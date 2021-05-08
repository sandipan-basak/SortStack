from django.urls import path, include
from SearchStack import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logged/', include(([
        path('search/', views.query_article, name='query'),
        path('folders/', views.FolderListView.as_view(), name='folders'),
        path('articles/', views.ArticleSetView.as_view(), name='set'),
    ], 'SearchStack'), namespace='search')),
]
"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from news.views import (
    NewsListView, NewsSearchView, NewsCreateView,
    NewsUpdateView, NewsDeleteView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView, CurrentPost
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),  # < вот тут
   path('news/', include('news.urls')),
   path('news/', NewsListView.as_view(), name='news-list'),
   path('news/search/', NewsSearchView.as_view(), name='news-search'),
   path('news/create/', NewsCreateView.as_view(), name='news-create'),
   path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news-update'),
   path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
   path('news/<int:pk>/', CurrentPost.as_view(), name='news-current'),

   path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
   path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-update'),
   path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]

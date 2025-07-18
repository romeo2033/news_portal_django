"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from accounts.views import become_author
from news.views import (ArticleCreateView, ArticleUpdateView, ArticleDeleteView
)

urlpatterns = [
    path('', include('news.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('become-author/', become_author, name='become_author'),
]

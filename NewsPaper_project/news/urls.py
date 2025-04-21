from django.urls import path, include
from .views import (
    NewsListView, NewsSearchView, NewsCreateView,
    NewsUpdateView, NewsDeleteView, CurrentPost, category_posts
)


urlpatterns = [
    path('', NewsListView.as_view(), name='news-list'),
    path('search/', NewsSearchView.as_view(), name='news-search'),
    path('create/', NewsCreateView.as_view(), name='news-create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('<int:pk>/', CurrentPost.as_view(), name='news-current'),
    path('category/<int:category_id>/', category_posts, name='category_posts'),
]

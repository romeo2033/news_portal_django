from django.urls import path
from .views import NewsList, CurrentPost

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', CurrentPost.as_view()),
]
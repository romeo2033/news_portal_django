from django.urls import path
from .views import IndexView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', IndexView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
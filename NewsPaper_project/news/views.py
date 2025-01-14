from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class NewsList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'news_list.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()

        return context


class CurrentPost(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

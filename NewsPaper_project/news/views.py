from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post
from .filters import NewsFilter

class NewsListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

class NewsSearchView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CurrentPost(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.type = 'NE'
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'NE':
            return HttpResponseForbidden("Изменение не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.delete_post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'NE':
            return HttpResponseForbidden("Удаление не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        form.instance.type = 'AR'
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'AR':
            return HttpResponseForbidden("Изменение не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.delete_post'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'AR':
            return HttpResponseForbidden("Удаление не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)
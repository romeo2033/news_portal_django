from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import render

from .models import Post, Category
from .filters import NewsFilter
from accounts.models import Author

from django.shortcuts import get_object_or_404, redirect, render


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created')
    return render(request, 'news/category_posts.html', {
        'category': category,
        'posts': posts,
    })

class NewsListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['time_now'] = timezone.now()
        ctx['selected_category'] = None
        return ctx

class NewsSearchView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        sub_id = request.GET.get('subscribe')
        if sub_id and request.user.is_authenticated:
            cat = get_object_or_404(Category, pk=sub_id)
            if request.user not in cat.subscribers.all():
                cat.subscribers.add(request.user)

        unsub_id = request.GET.get('unsubscribe')
        if unsub_id and request.user.is_authenticated:
            cat = get_object_or_404(Category, pk=unsub_id)
            if request.user in cat.subscribers.all():
                cat.subscribers.remove(request.user)

        if sub_id or unsub_id:
            params = request.GET.copy()
            params.pop('subscribe', None)
            params.pop('unsubscribe', None)
            return redirect(f"{request.path}?{params.urlencode()}")

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=qs)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filterset'] = self.filterset

        cat_id = self.request.GET.get('category')
        if cat_id:
            ctx['selected_category'] = get_object_or_404(Category, pk=cat_id)
        else:
            ctx['selected_category'] = None

        return ctx

class CurrentPost(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['category', 'title', 'content']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)
        now = timezone.now()
        start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = Post.objects.filter(
            author=author,
            created__gte=start_day
        ).count()

        if today_count >= 3:
            form.add_error(None, 'Вы уже создали три новости сегодня — лимит исчерпан.')
            return self.form_invalid(form)
        form.instance.type = 'NE'
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['category', 'title', 'content']
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
    fields = ['category', 'title', 'content']
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news-list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)
        now = timezone.now()
        start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = Post.objects.filter(
            author=author,
            created__gte=start_day
        ).count()

        if today_count >= 3:
            form.add_error(None, 'Вы уже создали три новости сегодня — лимит исчерпан.')
            return self.form_invalid(form)
        form.instance.type = 'AR'
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['category', 'title', 'content']
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
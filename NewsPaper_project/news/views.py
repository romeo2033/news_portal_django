from django.views.generic import ListView, DetailView
from .models import Post
from .filters import NewsFilter
from django.http import HttpResponseForbidden

class NewsListView(ListView):
    model = Post
    ordering = '-created'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

class NewsSearchView(ListView):
    model = Post
    ordering = '-created'
    template_name = 'news_list.html'  # можно использовать тот же шаблон
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()  # на случай, если фильтрация приводит к дубликатам

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем форму фильтров для отображения в шаблоне
        context['filterset'] = self.filterset
        return context


class CurrentPost(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post

# --- Для новостей ---
class NewsCreateView(CreateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']  # или перечислите необходимые поля
    template_name = 'news_form.html'
    success_url = reverse_lazy('news-list')  # имя url для списка новостей

    def form_valid(self, form):
        # Присваиваем полю type значение "новость" до сохранения объекта
        form.instance.type = 'NE'
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']  # или перечислите необходимые поля
    template_name = 'news_form.html'
    success_url = reverse_lazy('news-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'NE':
            return HttpResponseForbidden("Изменение не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news-list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'NE':
            return HttpResponseForbidden("Удаление не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

# --- Для статей (articles) ---
class ArticleCreateView(CreateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'article_form.html'
    success_url = reverse_lazy('news-list')

    def form_valid(self, form):
        # Присваиваем полю type значение "новость" до сохранения объекта
        form.instance.type = 'AR'
        return super().form_valid(form)
    # или укажите другой url, где будут выводиться статьи

class ArticleUpdateView(UpdateView):
    model = Post
    fields = ['author', 'category', 'title', 'content']
    template_name = 'article_form.html'
    success_url = reverse_lazy('news-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'AR':
            return HttpResponseForbidden("Изменение не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('news-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.type != 'AR':
            return HttpResponseForbidden("Удаление не разрешено для данного типа объекта.")
        return super().dispatch(request, *args, **kwargs)

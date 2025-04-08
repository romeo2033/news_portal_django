import django_filters
from django import forms
from .models import Post

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Заголовок"
    )
    # Если поле "author" – это связь с пользователем, то для поиска по имени можно искать по author.username
    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label="Автор"
    )
    created = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gt',  # фильтруем новости, созданные позже указанной даты
        label="Дата",
        widget=forms.DateInput(attrs={'type': 'date'})  # встроенный календарь
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created']
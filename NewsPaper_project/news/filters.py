import django_filters
from django import forms
from .models import Post


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Заголовок содержит:"
    )

    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label="Автор:"
    )

    created = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gt',
        label="После:",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created']
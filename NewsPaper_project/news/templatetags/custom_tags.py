from django import template
from news.models import Post


register = template.Library()


@register.simple_tag()
def news_counter():
    return Post.objects.count()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
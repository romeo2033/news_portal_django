import string
from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def censor(value):
    if type(value) != str:
        raise TypeError('The value must be a string')

    for word in value.translate(str.maketrans('', '', string.punctuation)).split():
        if len(word) > 1:
            if not word[1:].isupper() and not word[1:].islower():
                value = value.replace(word[1:-1], '*' * len(word[1:-1]))

    return value


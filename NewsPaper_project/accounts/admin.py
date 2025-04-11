from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Author
from news.models import Post

admin.site.register(Author)


def setup_author_group():
    authors_group, _ = Group.objects.get_or_create(name='authors')
    content_type = ContentType.objects.get_for_model(Post)
    add_perm = Permission.objects.get(codename='add_post', content_type=content_type)
    change_perm = Permission.objects.get(codename='change_post', content_type=content_type)
    authors_group.permissions.set([add_perm, change_perm])


setup_author_group()
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post, Category
from .tasks import notify_subscribers_for_post


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers_on_new_post(instance, action, **kwargs):
    if action != 'post_add':
        return
    notify_subscribers_for_post.delay(instance.id)
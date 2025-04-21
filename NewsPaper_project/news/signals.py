# news/signals.py

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import Post, Category

@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers_on_new_post(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    for cat_id in pk_set:
        category = Category.objects.get(pk=cat_id)
        for user in category.subscribers.all():
            subject = instance.title
            html = render_to_string('news/email/new_post_notification.html', {
                'post': instance,
                'category': category,
                'user': user,
            })
            text = strip_tags(html)
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html, "text/html")
            msg.send()
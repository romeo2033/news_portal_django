# news/tasks.py

from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from .models import Post, Category
from accounts.models import User  # или ваша модель пользователя


@shared_task
def send_welcome_email(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    subject = f'Добро пожаловать, {user.username}!'
    html = render_to_string('account/email/welcome_email.html', {
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


@shared_task
def notify_subscribers_for_post(post_id):
    post = Post.objects.get(pk=post_id)
    for category in post.category.all():
        for user in category.subscribers.all():
            html = render_to_string('news/email/new_post_notification.html', {
                'post': post,
                'category': category,
                'user': user,
            })
            text = strip_tags(html)
            msg = EmailMultiAlternatives(
                subject=post.title,
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html, "text/html")
            msg.send()


@shared_task
def weekly_digest():
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    for user in User.objects.all():
        posts = Post.objects.filter(
            category__subscribers=user,
            created__gte=one_week_ago
        ).distinct()
        if not posts:
            continue

        html = render_to_string('news/email/weekly_digest.html', {
            'user': user,
            'posts': posts,
        })
        text = strip_tags(html)
        msg = EmailMultiAlternatives(
            subject='Недельный дайджест',
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
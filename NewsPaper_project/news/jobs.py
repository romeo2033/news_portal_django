# news/jobs.py

from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from accounts.models import User
from .models import Post

def weekly_digest():
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    for user in User.objects.all():
        posts = Post.objects.filter(
            type=Post.news,
            category__subscribers=user,
            created__gte=one_week_ago
        ).distinct().order_by('-created')

        if not posts:
            continue

        html = render_to_string('news/email/weekly_digest.html', {
            'user': user,
            'posts': posts,
        })
        text = strip_tags(html)
        msg = EmailMultiAlternatives(
            subject='Ваш недельный дайджест новостей',
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
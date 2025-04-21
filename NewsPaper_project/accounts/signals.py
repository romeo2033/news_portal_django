from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()

@receiver(post_save, sender=User)
def add_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = f'Добро пожаловать, {user.username}!'
    html_content = render_to_string(
        'account/email/welcome_email.html',
        {
            'user': user,
            'activate_url': kwargs.get('action', None) or request.build_absolute_uri(),
        }
    )
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
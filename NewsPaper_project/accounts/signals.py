from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from news.tasks import send_welcome_email


User = get_user_model()


@receiver(post_save, sender=User)
def add_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)


@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    send_welcome_email.delay(user.id)
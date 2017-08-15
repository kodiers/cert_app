from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from .models import Profile


@receiver(post_save, sender=User)
def create_profile_and_token(sender, instance, created, *args, **kwargs):
    """
    Create token and profile
    """
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.authtoken.models import Token
from django_rest_passwordreset.signals import reset_password_token_created

from .models import Profile
from .tasks import send_password_reset_email


@receiver(post_save, sender=User)
def create_profile_and_token(sender, instance, created, *args, **kwargs):
    """
    Create token and profile
    """
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    reset_password_url = "{}?token={}".format(settings.FRONTEND_PASSWORD_RESET_URL, reset_password_token.key)
    send_password_reset_email.apply_async(args=[reset_password_token.user.username, reset_password_token.user.email,
                                                reset_password_url])

from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator

from common.models import BaseModel
from common.countries_list import COUNTRIES

# Create your models here.


class Profile(BaseModel):
    """
    User profile model
    """
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('User'), on_delete=models.CASCADE)
    country = models.CharField(max_length=5, choices=COUNTRIES, default='RU', verbose_name=_('Country'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    avatar = models.ImageField(upload_to='users', null=True, blank=True, verbose_name=_('Profile image'))

    def avatar_tag(self) -> str:
        return mark_safe('<img src="{}" height=75 width=75 />'.format(self.avatar.url))

    avatar_tag.short_description = _("Current image")
    avatar_tag.allow_tags = True

    @property
    def full_name(self) -> str:
        if self.user.first_name and self.user.last_name:
            return "{fn} {ln}".format(fn=self.user.first_name, ln=self.user.last_name)
        return self.user.username

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('created',)


class PasswordResetToken(BaseModel):
    """
    Password reset token model
    """
    token = models.CharField(max_length=64, db_index=True, unique=True, verbose_name=_('Token'))
    user = models.ForeignKey(User, related_name='reset_token', verbose_name=_('User'), on_delete=models.CASCADE)
    expire_at = models.DateTimeField(verbose_name='Token expires at')

    def _set_expiration_date(self):
        """
        Set password reset token expiration
        """
        self.expire_at = timezone.now() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRATION_PERIOD)

    @property
    def expired(self) -> bool:
        """
        Is token expired or not
        """
        now = timezone.now()
        return now > self.expire_at

    @staticmethod
    def create_password_reset_token(email: str) -> 'PasswordResetToken':
        """
        Create password reset token for user with email
        """
        user = User.objects.get(email=email)
        token_str = default_token_generator.make_token(user)
        token_obj = PasswordResetToken(token=token_str, user=user)
        token_obj._set_expiration_date()
        token_obj.save()
        return token_obj

from django.db import models
from django.utils.text import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel
from common.countries_list import COUNTRIES

# Create your models here.


class Profile(BaseModel):
    """
    User profile model
    """
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('Profile'), on_delete=models.CASCADE)
    country = models.CharField(max_length=5, choices=COUNTRIES, default='RU', verbose_name=_('Country'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    avatar = models.ImageField(upload_to='users', null=True, blank=True, verbose_name=_('Profile image'))

    def avatar_tag(self):
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

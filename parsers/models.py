from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel
from certifications.models import Vendor

# Create your models here.


class ParserConfig(BaseModel):
    """
    Model for configuration for parsers
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor'))
    url = models.URLField(verbose_name=_('URL'))
    parser_class_id = models.CharField(verbose_name='Parser ID', max_length=30, unique=True)

    def __str__(self):
        return f'{self.vendor.title} - {self.parser_class_id}'

    class Meta:
        verbose_name = _('Parser config')
        verbose_name_plural = _('Parser configs')
        ordering = ('created',)

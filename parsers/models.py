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
    main_url = models.URLField(verbose_name=_('Main URL'),
                               help_text='The main page, from which parsing should be started')
    base_url = models.URLField(verbose_name=_('Base url'), blank=True,
                               help_text='The url, which be added to certification paths.')
    parser_class_id = models.CharField(verbose_name='Parser ID', max_length=30, unique=True)
    certifications_link_css_selector = models.CharField(max_length=255, blank=True, default='',
                                                        verbose_name=_('Certifications link css selector'),
                                                        help_text=_('Selector to parse all links from main_url'))
    certification_title_css_selector = models.CharField(max_length=255, blank=True, default='',
                                                        verbose_name=_('Certification title css selector'))
    certification_description_css_selector = models.CharField(max_length=255, blank=True, default='',
                                                              verbose_name=_('Certification description css selector'))
    exam_title_css_selector = models.CharField(max_length=255, blank=True, default='',
                                               verbose_name=_('Exam title css selector'))
    exam_description_css_selector = models.CharField(max_length=255, blank=True, default='',
                                                     verbose_name=_('Exam description css selector'))

    def __str__(self):
        return f'{self.vendor.title} - {self.parser_class_id}'

    class Meta:
        verbose_name = _('Parser config')
        verbose_name_plural = _('Parser configs')
        ordering = ('created',)

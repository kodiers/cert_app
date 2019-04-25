from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel

# Create your models here.
# TODO: move common fields/methods to abstract model


class Vendor(BaseModel):
    """
    Vendor model
    """
    title = models.CharField(max_length=120, verbose_name=_("Title"), unique=True)
    image = models.ImageField(upload_to='vendors', null=True, blank=True, verbose_name=_('Vendor logo'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % self.image.url

    image_tag.short_description = _("Current image")
    image_tag.allow_tags = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        ordering = ('created',)


class Certification(BaseModel):
    """
    Certification model
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"), unique=True)
    number = models.CharField(max_length=20, verbose_name=_("Certification number"), null=True, blank=True)
    image = models.ImageField(upload_to='certifications', null=True, blank=True, verbose_name=_('Certification image'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    vendor = models.ForeignKey(Vendor, related_name='certifications', verbose_name=_("Vendor"),
                               on_delete=models.CASCADE)
    deprecated = models.BooleanField(default=False, verbose_name=_("Deprecated"))

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % self.image.url

    image_tag.short_description = _("Current image")
    image_tag.allow_tags = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Certification")
        verbose_name_plural = _("Certifications")
        ordering = ('created',)


class Exam(BaseModel):
    """
    Exam model
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"), unique=True)
    number = models.CharField(max_length=20, verbose_name=_("Exam number"), null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    certification = models.ManyToManyField(Certification, related_name='exams', verbose_name=_("Certification"))
    deprecated = models.BooleanField(default=False, verbose_name=_("Deprecated"))

    def __str__(self):
        return self.title

    @property
    def exam_full_title(self):
        if self.number:
            return "{} {}".format(self.number, self.title)
        return self.title

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")
        ordering = ('created',)
        unique_together = ('title', 'number')

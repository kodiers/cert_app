from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from common.models import BaseModel
from certifications.models import Certification, Exam

# Create your models here.


class UserCertification(BaseModel):
    """
    User certification model
    """
    user = models.ForeignKey(User, related_name='certifications', verbose_name=_("User"), on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, related_name='users_certifications',
                                      verbose_name=_("Certification"), on_delete=models.CASCADE)
    expiration_date = models.DateField(verbose_name=_("Expiration date"))
    remind_at_date = models.DateField(verbose_name=_("Remind at"), null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user.username, self.certification.title)

    class Meta:
        verbose_name = _("User's certification")
        verbose_name_plural = _("User's certifications")
        ordering = ("created",)
        unique_together = ('user', 'certification')


class UserExam(BaseModel):
    """
    User exam model
    """
    user = models.ForeignKey(User, related_name='exams', verbose_name=_("User"), on_delete=models.CASCADE)
    user_certification = models.ForeignKey(UserCertification, related_name="user_cert_exams",
                                           verbose_name=_("User certification"), on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name='users_exams', verbose_name=_("Exam"), on_delete=models.CASCADE)
    date_of_pass = models.DateField(verbose_name=_("Date of pass"))
    remind_at_date = models.DateField(verbose_name=_("Remind at"), null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user.username, self.exam.title)

    def save(self, *args, **kwargs):
        if self.exam not in self.user_certification.certification.exams.all():
            raise ValidationError("Exam is not part of selected certification")
        super(UserExam, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("User's exam")
        verbose_name_plural = _("User's exams")
        ordering = ("created",)
        unique_together = ('user', 'exam', 'user_certification')

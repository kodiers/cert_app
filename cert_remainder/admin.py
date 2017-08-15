from django.contrib import admin

from .models import UserCertification, UserExam

# Register your models here.


admin.site.register(UserCertification)
admin.site.register(UserExam)

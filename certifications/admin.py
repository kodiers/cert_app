from django.contrib import admin

from .models import Vendor, Certification, Exam

# Register your models here.


admin.site.register(Vendor)
admin.site.register(Certification)
admin.site.register(Exam)

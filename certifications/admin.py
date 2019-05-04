from django.contrib import admin

from .models import Vendor, Certification, Exam

# Register your models here.


class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'vendor', 'deprecated')
    search_fields = ('title', 'number')
    list_filter = ('vendor', 'deprecated')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'deprecated')
    search_fields = ('title', 'number', 'certification__title')
    list_filter = ('deprecated', 'certification__vendor')


admin.site.register(Vendor)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Exam, ExamAdmin)

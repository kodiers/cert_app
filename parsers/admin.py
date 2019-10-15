from django.contrib import admin

from .models import ParserConfig

# Register your models here.


class ParserConfigAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'main_url')
    search_fields = ('vendor__title', 'url', 'parser_class_id')


admin.site.register(ParserConfig, ParserConfigAdmin)

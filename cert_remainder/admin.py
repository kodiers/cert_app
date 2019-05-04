from django.contrib import admin

from .models import UserCertification, UserExam

# Register your models here.


class UserCertificationAdmin(admin.ModelAdmin):
    list_display = ('certification_title', 'certification_number', 'user', 'expiration_date', 'remind_at_date')
    search_fields = ('certification__title', 'certification__number', 'user__username', 'user__email')
    list_filter = ('certification__vendor',)
    sortable_by = ('user', 'expiration_date', 'remind_at_date')

    def certification_title(self, obj: UserCertification):
        return obj.certification.title

    def certification_number(self, obj: UserCertification):
        return obj.certification.number


class UserExamAdmin(admin.ModelAdmin):
    list_display = ('exam_title', 'exam_number', 'certification_title', 'user', 'date_of_pass', 'remind_at_date')
    search_fields = ('exam__title', 'exam__number', 'user_certification__certification__title', 'user__username',
                     'user__email')
    list_filter = ('user_certification__certification__vendor',)
    sortable_by = ('user', 'date_of_pass', 'remind_at_date')

    def exam_title(self, obj: UserExam):
        return obj.exam.title

    def exam_number(self, obj: UserExam):
        return obj.exam.number

    def certification_title(self, obj: UserExam):
        return obj.user_certification.certification.title


admin.site.register(UserCertification, UserCertificationAdmin)
admin.site.register(UserExam, UserExamAdmin)

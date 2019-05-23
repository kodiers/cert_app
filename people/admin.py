from django.contrib import admin

from .models import Profile, PasswordResetToken

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('avatar_tag',)
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'user_email')

    def user_email(self, obj: Profile):
        return obj.user.email


class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expire_at', 'expired')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'expire_at'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)

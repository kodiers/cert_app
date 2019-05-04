from django.contrib import admin

from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('avatar_tag',)
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'user_email')

    def user_email(self, obj: Profile):
        return obj.user.email


admin.site.register(Profile, ProfileAdmin)

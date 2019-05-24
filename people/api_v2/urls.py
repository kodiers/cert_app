from django.urls import path

from .views import UserRegistrationAPIViewV2, RequestPasswordResetTokenAPIViewV2


app_name = 'people_api_v2'

urlpatterns = (
    path('register/', UserRegistrationAPIViewV2.as_view(), name='registration'),
    path('password/reset/', RequestPasswordResetTokenAPIViewV2.as_view(), name='password_reset')
)

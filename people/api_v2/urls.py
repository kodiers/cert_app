from django.urls import path, include

from .views import UserRegistrationAPIViewV2


app_name = 'people_api_v2'

urlpatterns = (
    path('register/', UserRegistrationAPIViewV2.as_view(), name='registration'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))
)

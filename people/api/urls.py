from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from .views import UserRegistrationAPIView, GetUserInfoAPIView


app_name = 'people_api'

urlpatterns = (
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('register/', UserRegistrationAPIView.as_view(), name='registration'),
    path('user/', GetUserInfoAPIView.as_view(), name='user')
)

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from .views import UserRegistrationAPIView, GetUserInfoAPIView


urlpatterns = (
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^register/$', UserRegistrationAPIView.as_view(), name='registration'),
    url(r'^user/$', GetUserInfoAPIView.as_view(), name='user')
)

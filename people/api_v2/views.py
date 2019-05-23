from django.contrib.auth import logout

from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

from people.models import Profile
from people.tasks import send_registration_confirmation, send_password_reset_email
from people.api.serializers import ProfileSerializer

from .serializers import UserRegistrationSerializerV2, RequestPasswordResetSerializer


class UserRegistrationAPIViewV2(GenericAPIView):
    """
    User registration API view. Accept post. Require username, email, password, confirm_password
    """
    serializer_class = UserRegistrationSerializerV2
    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request) -> Response:
        logout(request)
        serializer = UserRegistrationSerializerV2(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profile.objects.get(user=user)
        profile_serializer = ProfileSerializer(profile)
        send_registration_confirmation.delay(user.username, user.email)
        return Response(profile_serializer.data, status=status.HTTP_201_CREATED)


class RequestPasswordResetTokenAPIViewV2(CreateAPIView):
    """
    Request password reset token
    """
    serializer_class = RequestPasswordResetSerializer
    parser_classes = (JSONParser, )
    permission_classes = (permissions.AllowAny,)

    def create(self, request: Request, *args: str, **kwargs: str) -> Response:
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        send_password_reset_email.delay(instance.user.username, instance.user.email, instance.token)
        return Response({'result': "Ok", 'message': 'Password reset email was sent.'}, status=status.HTTP_201_CREATED)

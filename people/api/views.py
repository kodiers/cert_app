from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from django.contrib.auth import logout

from people.models import Profile

from .serializers import UserRegistrationSerializer, ProfileSerializer


class UserRegistrationAPIView(GenericAPIView):
    """
    User registration API view. Accept post. Require username, password, confirm_password
    """
    serializer_class = UserRegistrationSerializer
    parser_classes = (JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Handle HttpRequest (post)
        :param request: httpRequest (Require username, password, confirm_password fields)
        :return: HttpResponse (serialized Profile)
        """
        logout(request)
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profile.objects.get(user=user)
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data, status=status.HTTP_201_CREATED)


class GetUserInfoAPIView(GenericAPIView):
    """
    Get info about authenticated user
    """
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

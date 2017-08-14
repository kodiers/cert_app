from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from cert_remainder.models import UserCertification, UserExam

from .serializers import UserCertificationSerializer, UserExamSerializer


class UserCertificationListCreateAPIView(ListCreateAPIView):
    """
    User certification list create api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCertificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('certification', 'expiration_date', 'remind_at_date')

    def get_queryset(self):
        queryset = UserCertification.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = UserCertificationSerializer(data=request.data, context=context, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCertificationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get user certification api view by id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCertificationSerializer

    def get_queryset(self):
        queryset = UserCertification.objects.filter(user=self.request.user)
        return queryset


class UserExamListCreateAPIView(ListCreateAPIView):
    """
    User exams list create api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_certification__certification', 'date_of_pass', 'remind_at_date')

    def get_queryset(self):
        queryset = UserExam.objects.filter(user=self.request.user)
        return queryset


class UserExamRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get user exams api view by id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserExamSerializer

    def get_queryset(self):
        queryset = UserExam.objects.filter(user=self.request.user)
        return queryset

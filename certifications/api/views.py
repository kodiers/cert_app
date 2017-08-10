from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend

from certifications.models import Vendor, Certification, Exam

from .serializers import VendorSerializer, CertificationSerializer, ExamSerializer


class VendorListAPIView(ListAPIView):
    """
    Vendor list api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve vendor by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class CertificationListCreateAPIView(ListCreateAPIView):
    """
    Certification list create api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('vendor',)
    parser_classes = (JSONParser, MultiPartParser, FormParser)


class CertificationRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve certification by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class ExamListCreateAPIView(ListCreateAPIView):
    """
    Exam list create api view
    """
    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('certification', 'certification__vendor')


class ExamRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve exam by id
    """
    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

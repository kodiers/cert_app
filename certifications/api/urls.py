from django.urls import path

from .views import (
    VendorListAPIView,
    VendorRetrieveAPIView,
    CertificationListCreateAPIView,
    CertificationRetrieveAPIView,
    ExamListCreateAPIView,
    ExamRetrieveAPIView,
    AddCertificationToExamUpdateAPIView
)


app_name = 'certifications_api'

urlpatterns = (
    path('vendor/', VendorListAPIView.as_view(), name='vendors'),
    path('vendor/<int:pk>/', VendorRetrieveAPIView.as_view(), name='vendor'),
    path('certification/', CertificationListCreateAPIView.as_view(), name='certifications'),
    path('certification/<int:pk>/', CertificationRetrieveAPIView.as_view(), name='certification'),
    path('exam/', ExamListCreateAPIView.as_view(), name='exams'),
    path('exam/<int:pk>/', ExamRetrieveAPIView.as_view(), name='exam'),
    path('exam/add/<int:pk>/', AddCertificationToExamUpdateAPIView.as_view(), name='add_cert_to_exam')
)

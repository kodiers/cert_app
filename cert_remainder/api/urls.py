from django.urls import path

from .views import (
    UserCertificationListCreateAPIView,
    UserCertificationRetrieveUpdateDestroyAPIView,
    UserExamListCreateAPIView,
    UserExamRetrieveUpdateDestroyAPIView,
    BulkUserExamCreateAPIView,
    BulkUserExamUpdateAPIView
)


app_name = 'cert_remainder_api'

urlpatterns = (
    path('certification/', UserCertificationListCreateAPIView.as_view(), name='user_certifications'),
    path('certification/<int:pk>/', UserCertificationRetrieveUpdateDestroyAPIView.as_view(), name='user_certification'),
    path('exam/', UserExamListCreateAPIView.as_view(), name='user_exams'),
    path('exam/<int:pk>/', UserExamRetrieveUpdateDestroyAPIView.as_view(), name='user_exam'),
    path('exam/bulk/create/', BulkUserExamCreateAPIView.as_view(), name='bulk_create_user_exams'),
    path('exam/bulk/update/', BulkUserExamUpdateAPIView.as_view(), name='bulk_update_user_exams')
)

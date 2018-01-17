from django.conf.urls import url

from .views import (
    UserCertificationListCreateAPIView,
    UserCertificationRetrieveUpdateDestroyAPIView,
    UserExamListCreateAPIView,
    UserExamRetrieveUpdateDestroyAPIView,
    BulkUserExamCreateAPIView,
    BulkUserExamUpdateAPIView
)


urlpatterns = (
    url(r'^certification/$', UserCertificationListCreateAPIView.as_view(), name='user_certifications'),
    url(r'^certification/(?P<pk>\d+)/$', UserCertificationRetrieveUpdateDestroyAPIView.as_view(),
        name='user_certification'),
    url(r'^exam/$', UserExamListCreateAPIView.as_view(), name='user_exams'),
    url(r'^exam/(?P<pk>\d+)/$', UserExamRetrieveUpdateDestroyAPIView.as_view(), name='user_exam'),
    url(r'^exam/bulk/create/$', BulkUserExamCreateAPIView.as_view(), name='bulk_create_user_exams'),
    url(r'^exam/bulk/update/$', BulkUserExamUpdateAPIView.as_view(), name='bulk_update_user_exams')
)

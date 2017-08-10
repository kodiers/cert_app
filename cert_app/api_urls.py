from django.conf.urls import url, include

urlpatterns = (
    url(r'^people/', include('people.api.urls', namespace='people_api')),
    url(r'^certifications/', include('certifications.api.urls', namespace='certifications_api'))
)

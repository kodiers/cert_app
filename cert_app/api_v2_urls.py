from django.urls import path, include


app_name = 'api_v2'


urlpatterns = (
    path('people/', include('people.api_v2.urls', namespace='people_api_v2')),
)

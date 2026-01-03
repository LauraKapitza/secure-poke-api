from django.urls import path, include

urlpatterns = [
    path("api/", include("access_management_api.urls")),
]

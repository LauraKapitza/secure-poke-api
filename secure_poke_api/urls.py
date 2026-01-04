from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("access_management_api.urls")),
    path("api/", include("pokemon_api.urls")),
]
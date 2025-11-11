from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MeView, add_group, remove_group


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("user/me/", MeView.as_view(), name="me"),
    path("group/<str:pokemon_type>/add/", add_group, name="add_group"),
    path("group/<str:pokemon_type>/remove/", remove_group, name="remove_group")
]
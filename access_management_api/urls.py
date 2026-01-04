from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import MeView, AddGroupView, RemoveGroupView


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("user/me/", MeView.as_view(), name="me"),
    path("group/<str:pokemon_type>/add/", AddGroupView.as_view(), name="add_group"),
    path("group/<str:pokemon_type>/remove/", RemoveGroupView.as_view(), name="remove_group")
]

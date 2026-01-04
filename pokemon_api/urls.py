from django.urls import path
from .views import PokemonDetailView, PokemonListView


urlpatterns = [
    path("pokemon/", PokemonListView.as_view(), name="pokemon_list"),
    path("pokemon/<str:identifier>/", PokemonDetailView.as_view(), name="pokemon_detail"),
]

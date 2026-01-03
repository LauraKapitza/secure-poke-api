from django.apps import AppConfig
from .utils.pokemon_types import load_pokemon_types


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_management_api'

    def ready(self):
        load_pokemon_types()

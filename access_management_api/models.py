from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # User inherits username, password, etc.
    pass


class PokemonTypeGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name="pokemon_groups")

    def __str__(self):
        return self.name

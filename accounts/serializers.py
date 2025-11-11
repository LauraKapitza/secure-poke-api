from rest_framework import serializers
from .models import User, PokemonTypeGroup


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonTypeGroup
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    pokemon_groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "pokemon_groups"]

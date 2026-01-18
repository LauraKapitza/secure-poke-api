from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PokemonTypeGroup
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from access_management_api.services.load_pokemon_types import load_pokemon_types

User = get_user_model()


class MeView(generics.RetrieveAPIView):
    """
        GET /api/user/me
        Gets current user with their Pokémon type groups.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddGroupView(APIView):
    """
        POST /api/group/<pokemon_type>/add
        Adds a valid Pokémon type group to user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        pokemon_type = pokemon_type.lower()
        allowed_types = load_pokemon_types()

        if pokemon_type not in allowed_types:
            return Response(
                {"error": f"Invalid Pokémon type: '{pokemon_type}'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        group, _created = PokemonTypeGroup.objects.get_or_create(name=pokemon_type)
        user.pokemon_groups.add(group)
        return Response(
            {"message": f"Added {pokemon_type} group"},
            status=status.HTTP_200_OK
        )


class RemoveGroupView(APIView):
    """
        POST /api/group/<pokemon_type>/remove
        Removes a Pokémon type group from user.
        Since the action only removes a group from the current user and not a deletion, the endpoint is a POST.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        user = request.user
        try:
            group = PokemonTypeGroup.objects.get(name=pokemon_type)
            user.pokemon_groups.remove(group)
            return Response(
                {"message": f"Removed {pokemon_type} group"},
                status=status.HTTP_200_OK
            )
        except PokemonTypeGroup.DoesNotExist:
            return Response(
                {"error": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )

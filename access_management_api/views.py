from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PokemonTypeGroup
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

from .utils.pokemon_types import POKEMON_TYPES

User = get_user_model()


# GET /api/user/me
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# POST /api/group/<pokemon_type>/add
class AddGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        pokemon_type = pokemon_type.lower()

        if pokemon_type not in POKEMON_TYPES:
            return Response(
                {"error": f"Invalid Pokémon type '{pokemon_type}'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        group, _created = PokemonTypeGroup.objects.get_or_create(name=pokemon_type)
        user.pokemon_groups.add(group)
        return Response(
            {"message": f"Added {pokemon_type} group"},
            status=status.HTTP_200_OK
        )


# POST /api/group/<pokemon_type>/remove
# Since the action only removes a group from the current user and not a deletion, the endpoint is a POST
class RemoveGroupView(APIView):
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

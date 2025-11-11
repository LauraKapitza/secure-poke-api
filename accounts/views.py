from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PokemonTypeGroup
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# GET /api/user/me
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# POST /api/group/<pokemon_type>/add
# Since the action only removes a group from the current user and not a deletion, the endpoint is a POST
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_group(request, pokemon_type):
    user = request.user
    group, created = PokemonTypeGroup.objects.get_or_create(name=pokemon_type)
    user.pokemon_groups.add(group)
    return Response({"message": f"Added to {pokemon_type} group"})


# POST /api/group/<pokemon_type>/remove
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_group(request, pokemon_type):
    user = request.user
    try:
        group = PokemonTypeGroup.objects.get(name=pokemon_type)
        user.pokemon_groups.remove(group)
        return Response({"message": f"Removed from {pokemon_type} group"})
    except PokemonTypeGroup.DoesNotExist:
        return Response({"error": "Group not found"}, status=404)

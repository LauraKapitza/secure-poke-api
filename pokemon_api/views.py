from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from pokemon_api.services.fetch_pokemon import fetch_pokemon
from pokemon_api.services.fetch_pokemon_by_type import fetch_pokemon_by_type


class PokemonListView(APIView):
    """
    GET /api/pokemon/
    Returns all Pokémon the user is allowed to access,
    based on the Pokémon types they belong to.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        allowed_types = {g.name for g in user.pokemon_groups.all()}

        if not allowed_types:
            return Response([], status=status.HTTP_200_OK)

        # Collect Pokémon from all allowed types
        pokemon_set = {}

        for pokemon_type in allowed_types:
            pokemon_entries = fetch_pokemon_by_type(pokemon_type)

            for entry in pokemon_entries:
                name = entry["name"]
                pokemon_set[name] = {
                    "name": name,
                    "url": f"/api/pokemon/{name}/"
                }

        # Convert dict to list
        pokemon_list = list(pokemon_set.values())

        return Response(pokemon_list, status=status.HTTP_200_OK)


class PokemonDetailView(APIView):
    """
    GET /api/pokemon/<id or name>/
    Returns details for a single Pokémon,
    only if the user has access to at least one of its types.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, identifier):
        user = request.user
        allowed_types = {g.name for g in user.pokemon_groups.all()}

        pokemon_data = fetch_pokemon(identifier)

        if pokemon_data is None:
            return Response(
                {"error": "Pokémon not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Extract Pokémon types
        pokemon_types = {
            t["type"]["name"]
            for t in pokemon_data.get("types", [])
        }

        # Check access
        if not (pokemon_types & allowed_types):
            return Response(
                {"error": "Forbidden: you do not have access to this Pokémon"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(pokemon_data, status=status.HTTP_200_OK)

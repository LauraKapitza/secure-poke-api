import requests

POKEMON_TYPES = None


def load_pokemon_types():
    global POKEMON_TYPES

    if POKEMON_TYPES is not None:
        return POKEMON_TYPES

    try:
        response = requests.get("https://pokeapi.co/api/v2/type/")
        response.raise_for_status()
        data = response.json()
        POKEMON_TYPES = {t["name"] for t in data["results"]}
    except Exception:
        POKEMON_TYPES = set()

    return POKEMON_TYPES

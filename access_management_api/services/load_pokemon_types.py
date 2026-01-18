import requests

POKEMON_TYPES = None

DEFAULT_POKEMON_TYPES = [
    "normal", "fighting", "flying", "poison", "ground",
    "rock", "bug", "ghost", "steel", "fire",
    "water", "grass", "electric", "psychic", "ice",
    "dragon", "dark", "fairy", "stellar", "unknown"
]


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
        POKEMON_TYPES = DEFAULT_POKEMON_TYPES

    return POKEMON_TYPES

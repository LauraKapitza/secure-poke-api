import requests

POKEMON_TYPES = set()

def load_pokemon_types():
    global POKEMON_TYPES
    try:
        response = requests.get("https://pokeapi.co/api/v2/type/")
        response.raise_for_status()
        data = response.json()
        POKEMON_TYPES = {t["name"] for t in data["results"]}
    except Exception:
        # Fallback: empty set → validation will fail safely
        POKEMON_TYPES = set()

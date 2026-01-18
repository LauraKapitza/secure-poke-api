import requests


def fetch_pokemon(identifier):
    """
    Fetch a Pokémon from the official PokeAPI.
    Returns None if not found.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{identifier}/"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()

import requests

def fetch_pokemon_by_type(pokemon_type):
    """
    Fetch all Pokémon belonging to a given type.
    Returns a list of dicts: [{ "name": "...", "url": "..." }, ...]
    """
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type}/"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    return [
        entry["pokemon"]
        for entry in data.get("pokemon", [])
    ]
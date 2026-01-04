from unittest.mock import patch, MagicMock
from django.test import TestCase
import access_management_api.utils.load_pokemon_types as pokemon_types


class LoadPokemonTypesTest(TestCase):
    def setUp(self):
        pokemon_types.POKEMON_TYPES = None

    @patch("access_management_api.utils.load_pokemon_types.requests.get")
    def test_load_pokemon_types_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"name": "fire"},
                {"name": "water"},
                {"name": "grass"},
            ]
        }
        mock_get.return_value = mock_response

        result = pokemon_types.load_pokemon_types()

        self.assertEqual(result, {"fire", "water", "grass"})
        self.assertEqual(pokemon_types.POKEMON_TYPES, {"fire", "water", "grass"})

    @patch("access_management_api.utils.load_pokemon_types.requests.get")
    def test_load_pokemon_types_api_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = pokemon_types.load_pokemon_types()

        self.assertEqual(result, set())
        self.assertEqual(pokemon_types.POKEMON_TYPES, set())

    @patch("access_management_api.utils.load_pokemon_types.requests.get")
    def test_load_pokemon_types_invalid_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = pokemon_types.load_pokemon_types()

        self.assertEqual(result, set())
        self.assertEqual(pokemon_types.POKEMON_TYPES, set())

    @patch("access_management_api.utils.load_pokemon_types.requests.get")
    def test_load_pokemon_types_empty_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result = pokemon_types.load_pokemon_types()

        self.assertEqual(result, set())
        self.assertEqual(pokemon_types.POKEMON_TYPES, set())

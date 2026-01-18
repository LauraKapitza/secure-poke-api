from unittest.mock import patch, MagicMock
from django.test import TestCase

from pokemon_api.services.fetch_pokemon import fetch_pokemon
from pokemon_api.services.fetch_pokemon_by_type import fetch_pokemon_by_type


class FetchPokemonTest(TestCase):

    @patch("pokemon_api.services.fetch_pokemon.requests.get")
    def test_fetch_pokemon_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "pikachu"}
        mock_get.return_value = mock_response

        result = fetch_pokemon("pikachu")

        self.assertEqual(result, {"name": "pikachu"})
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/pikachu/")

    @patch("pokemon_api.services.fetch_pokemon.requests.get")
    def test_fetch_pokemon_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_pokemon("missingmon")

        self.assertIsNone(result)

    @patch("pokemon_api.services.fetch_pokemon.requests.get")
    def test_fetch_pokemon_server_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = fetch_pokemon("pikachu")

        self.assertIsNone(result)


class FetchPokemonByTypeTest(TestCase):

    @patch("pokemon_api.services.fetch_pokemon_by_type.requests.get")
    def test_fetch_pokemon_by_type_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "pokemon": [
                {"pokemon": {"name": "charmander", "url": "dummy"}},
                {"pokemon": {"name": "vulpix", "url": "dummy"}},
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_pokemon_by_type("fire")

        self.assertEqual(
            result,
            [
                {"name": "charmander", "url": "dummy"},
                {"name": "vulpix", "url": "dummy"},
            ]
        )
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/type/fire/")

    @patch("pokemon_api.services.fetch_pokemon_by_type.requests.get")
    def test_fetch_pokemon_by_type_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_pokemon_by_type("unknown")

        self.assertEqual(result, [])

    @patch("pokemon_api.services.fetch_pokemon_by_type.requests.get")
    def test_fetch_pokemon_by_type_empty_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pokemon": []}
        mock_get.return_value = mock_response

        result = fetch_pokemon_by_type("fire")

        self.assertEqual(result, [])

    @patch("pokemon_api.services.fetch_pokemon_by_type.requests.get")
    def test_fetch_pokemon_by_type_missing_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # no "pokemon" key
        mock_get.return_value = mock_response

        result = fetch_pokemon_by_type("fire")

        self.assertEqual(result, [])

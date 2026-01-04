from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from access_management_api.models import PokemonTypeGroup

User = get_user_model()


class PokemonAPITest(APITestCase):

    def setUp(self):
        # Create a test user
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        # Login to get JWT token
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            {"username": self.username, "password": self.password},
            format="json"
        )
        self.token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # ---------------------------------------------------------
    # LIST VIEW TESTS
    # ---------------------------------------------------------

    @patch("pokemon_api.views.fetch_pokemon_by_type")
    def test_list_pokemon_with_no_groups_returns_empty_list(self, mock_fetch):
        url = reverse("pokemon_list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        mock_fetch.assert_not_called()

    @patch("pokemon_api.views.fetch_pokemon_by_type")
    def test_list_pokemon_with_one_group(self, mock_fetch):
        # User belongs to "fire"
        group = PokemonTypeGroup.objects.create(name="fire")
        self.user.pokemon_groups.add(group)

        # Mock PokeAPI response
        mock_fetch.return_value = [
            {"name": "charmander", "url": "dummy"},
            {"name": "vulpix", "url": "dummy"},
        ]

        url = reverse("pokemon_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "charmander")

    @patch("pokemon_api.views.fetch_pokemon_by_type")
    def test_list_pokemon_deduplicates_across_types(self, mock_fetch):
        # User belongs to fire + flying
        fire = PokemonTypeGroup.objects.create(name="fire")
        flying = PokemonTypeGroup.objects.create(name="flying")
        self.user.pokemon_groups.add(fire, flying)

        # Mock responses
        mock_fetch.side_effect = [
            [{"name": "charizard", "url": "dummy"}],  # fire
            [{"name": "charizard", "url": "dummy"}],  # flying
        ]

        url = reverse("pokemon_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # deduplicated
        self.assertEqual(response.data[0]["name"], "charizard")

    # ---------------------------------------------------------
    # DETAIL VIEW TESTS
    # ---------------------------------------------------------

    @patch("pokemon_api.views.fetch_pokemon")
    def test_detail_pokemon_not_found(self, mock_fetch):
        mock_fetch.return_value = None

        url = reverse("pokemon_detail", kwargs={"identifier": "missingmon"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("pokemon_api.views.fetch_pokemon")
    def test_detail_pokemon_forbidden(self, mock_fetch):
        # User has no groups
        mock_fetch.return_value = {
            "name": "squirtle",
            "types": [{"type": {"name": "water"}}]
        }

        url = reverse("pokemon_detail", kwargs={"identifier": "squirtle"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("pokemon_api.views.fetch_pokemon")
    def test_detail_pokemon_allowed(self, mock_fetch):
        # User belongs to water
        group = PokemonTypeGroup.objects.create(name="water")
        self.user.pokemon_groups.add(group)

        mock_fetch.return_value = {
            "name": "squirtle",
            "types": [{"type": {"name": "water"}}]
        }

        url = reverse("pokemon_detail", kwargs={"identifier": "squirtle"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "squirtle")

    @patch("pokemon_api.views.fetch_pokemon")
    def test_detail_pokemon_multi_type_allowed(self, mock_fetch):
        # User belongs to flying
        group = PokemonTypeGroup.objects.create(name="flying")
        self.user.pokemon_groups.add(group)

        mock_fetch.return_value = {
            "name": "charizard",
            "types": [
                {"type": {"name": "fire"}},
                {"type": {"name": "flying"}}
            ]
        }

        url = reverse("pokemon_detail", kwargs={"identifier": "charizard"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "charizard")

    # ---------------------------------------------------------
    # AUTH TESTS
    # ---------------------------------------------------------

    def test_list_requires_authentication(self):
        self.client.credentials()  # remove token
        url = reverse("pokemon_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_requires_authentication(self):
        self.client.credentials()  # remove token
        url = reverse("pokemon_detail", kwargs={"identifier": "pikachu"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

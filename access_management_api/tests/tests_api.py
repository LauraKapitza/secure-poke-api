from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from access_management_api.models import PokemonTypeGroup
from unittest.mock import patch

User = get_user_model()


class AccountsAPITest(APITestCase):

    def setUp(self):
        # Create a test user
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        # Endpoints
        self.login_url = reverse("login")
        self.me_url = reverse("me")

    def authenticate(self):
        """Helper method to log in and set JWT token."""
        response = self.client.post(
            self.login_url,
            {"username": self.username, "password": self.password},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]

        # Set Authorization header for all future requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # -----------------------------
    # LOGIN TESTS
    # -----------------------------
    def test_login_returns_jwt_token(self):
        response = self.client.post(
            self.login_url,
            {"username": self.username, "password": self.password},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_fails_with_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"username": self.username, "password": "wrong_password"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fails_with_missing_fields(self):
        response = self.client.post(self.login_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -----------------------------
    # /user/me TESTS
    # -----------------------------

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user_data_when_authenticated(self):
        self.authenticate()
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.username)
        self.assertIn("pokemon_groups", response.data)

    def test_me_fails_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid token")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -----------------------------
    # ADD POKEMON GROUP TESTS
    # -----------------------------

    @patch("access_management_api.utils.load_pokemon_types.POKEMON_TYPES", {"fire", "water"})
    def test_add_group_valid_type(self):
        self.authenticate()
        url = reverse("add_group", kwargs={"pokemon_type": "fire"})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PokemonTypeGroup.objects.filter(name="fire", users=self.user).exists())

    def test_add_group_requires_authentication(self):
        url = reverse("add_group", kwargs={"pokemon_type": "fire"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_group_twice(self):
        self.authenticate()
        url = reverse("add_group", kwargs={"pokemon_type": "grass"})
        self.client.post(url)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Still only one group instance
        self.assertEqual(PokemonTypeGroup.objects.filter(name="grass").count(), 1)

    def test_add_group_wrong_method(self):
        self.authenticate()
        url = reverse("add_group", kwargs={"pokemon_type": "fire"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # -----------------------------
    # REMOVE GROUP TESTS
    # -----------------------------
    def test_remove_group(self):
        self.authenticate()

        # First add the group
        group = PokemonTypeGroup.objects.create(name="water")
        self.user.pokemon_groups.add(group)

        url = reverse("remove_group", kwargs={"pokemon_type": "water"})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            PokemonTypeGroup.objects.filter(name="water", users=self.user).exists()
        )

    def test_remove_group_not_found(self):
        self.authenticate()
        url = reverse("remove_group", kwargs={"pokemon_type": "unknown"})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_group_user_not_in_group(self):
        self.authenticate()
        PokemonTypeGroup.objects.create(name="electric")  # exists but user is not in it
        url = reverse("remove_group", kwargs={"pokemon_type": "electric"})
        response = self.client.post(url)
        # Should still return 200, but user remains not in group
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse( PokemonTypeGroup.objects.filter(name="electric", users=self.user).exists() )

    def test_remove_group_requires_authentication(self):
        url = reverse("remove_group", kwargs={"pokemon_type": "water"})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_group_wrong_method(self):
        self.authenticate()
        url = reverse("remove_group", kwargs={"pokemon_type": "water"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

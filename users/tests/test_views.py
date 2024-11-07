from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.test import TestCase

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_list_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_authenticated(self):
        self.client.force_authenticate(user=self.user)

        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post("/users/", new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_unauthenticated(self):
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post("/users/", new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_unauthenticated(self):
        response = self.client.get("/users/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_update_authenticated(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
        }

        response = self.client.patch("/users/me/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["last_name"], "User")

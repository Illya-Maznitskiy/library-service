from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from books.models import Book


User = get_user_model()


class BookViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="user",
            password="password",
            email="user@example.com",
            is_staff=False,
        )
        self.book_data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": "SOFT",
            "inventory": 10,
            "daily_fee": "1.50",
        }
        self.book = Book.objects.create(**self.book_data)

    def test_get_books(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/books/", self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/books/", self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {"title": "Animal Farm"}
        response = self.client.patch(
            f"/books/{self.book.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Animal Farm")

    def test_update_book_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        updated_data = {"title": "Animal Farm"}
        response = self.client.patch(
            f"/books/{self.book.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

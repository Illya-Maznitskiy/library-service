from rest_framework.test import APITestCase

from books.models import Book
from books.serializers import BookSerializer


class BookSerializerTest(APITestCase):

    def setUp(self):
        self.book_data = {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "cover": "HARD",
            "inventory": 5,
            "daily_fee": "2.00",
        }
        self.book = Book.objects.create(**self.book_data)

    def test_serializer_fields(self):
        serializer = BookSerializer(instance=self.book)
        self.assertEqual(
            set(serializer.data.keys()),
            {"id", "title", "author", "cover", "inventory", "daily_fee"},
        )

    def test_serializer_data(self):
        serializer = BookSerializer(instance=self.book)
        for field_name, field_value in self.book_data.items():
            self.assertEqual(serializer.data[field_name], field_value)

    def test_serializer_validation(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["title"], "The Catcher in the Rye"
        )

    def test_serializer_invalid_data(self):
        invalid_data = self.book_data.copy()
        invalid_data["inventory"] = -5  # Invalid: should be a positive integer
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("inventory", serializer.errors)

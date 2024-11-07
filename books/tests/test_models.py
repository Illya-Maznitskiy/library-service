from django.test import TestCase

from books.models import Book


class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover="HARD",
            inventory=10,
            daily_fee=1.50,
        )

    def test_book_creation(self):
        book = Book.objects.get(title="The Great Gatsby")
        self.assertEqual(book.author, "F. Scott Fitzgerald")
        self.assertEqual(book.cover, "HARD")
        self.assertEqual(book.inventory, 10)
        self.assertEqual(book.daily_fee, 1.50)

    def test_str_method(self):
        self.assertEqual(str(self.book), "The Great Gatsby")

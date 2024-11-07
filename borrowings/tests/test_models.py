from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from books.models import Book
from users.models import User
from borrowings.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=5.00,
        )

        self.borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date()
            + timezone.timedelta(days=7),
            book=self.book,
            user=self.user,
        )

    def test_borrowing_creation(self):
        self.assertEqual(self.borrowing.book, self.book)
        self.assertEqual(self.borrowing.user, self.user)
        self.assertEqual(self.borrowing.borrow_date, timezone.now().date())
        self.assertEqual(
            self.borrowing.expected_return_date,
            timezone.now().date() + timezone.timedelta(days=7),
        )

    def test_borrowing_str(self):
        self.assertEqual(
            str(self.borrowing), f"Borrowed on {self.borrowing.borrow_date}"
        )

    def test_actual_return_date_optional(self):
        self.assertIsNone(self.borrowing.actual_return_date)

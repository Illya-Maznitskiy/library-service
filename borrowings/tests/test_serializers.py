from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BookDetailSerializer,
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


User = get_user_model()


class BookDetailSerializerTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="Paperback",
            inventory=5,
            daily_fee=10.0,
        )

    def test_book_detail_serializer_fields(self):
        serializer = BookDetailSerializer(instance=self.book)
        self.assertEqual(
            set(serializer.data.keys()),
            {"id", "title", "author", "cover", "inventory", "daily_fee"},
        )


class BorrowingSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="Paperback",
            inventory=1,
            daily_fee=10.0,
        )

    def test_borrowing_serializer_valid_data(self):
        borrow_date = date.today()
        expected_return_date = borrow_date + timedelta(days=1)

        data = {
            "book": self.book.id,
            "borrow_date": borrow_date,
            "expected_return_date": expected_return_date,
            "user": self.user.id,
        }

        self.client.force_authenticate(user=self.user)

        request = APIRequestFactory().post("/fake-url/")
        request.user = self.user

        serializer = BorrowingSerializer(
            data=data, context={"request": request}
        )

        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)
            return

        borrowing = serializer.save()

        self.assertEqual(self.book.inventory, 1)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.borrow_date, borrow_date)
        self.assertEqual(borrowing.expected_return_date, expected_return_date)

    def test_borrowing_serializer_date_validation(self):
        borrow_date = date.today()
        expected_return_date = borrow_date - timedelta(days=1)

        data = {
            "book": self.book.id,
            "borrow_date": borrow_date,
            "expected_return_date": expected_return_date,
            "user": self.user.id,
        }

        self.client.force_authenticate(user=self.user)

        serializer = BorrowingSerializer(
            data=data, context={"request": self.client.request}
        )

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "Expected return date must be after borrow date.",
            str(context.exception),
        )


class BorrowingDetailSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="Paperback",
            inventory=1,
            daily_fee=10.0,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
        )

    def test_borrowing_detail_serializer_fields(self):
        serializer = BorrowingDetailSerializer(instance=self.borrowing)
        self.assertEqual(
            set(serializer.data.keys()),
            {
                "book",
                "user",
                "borrow_date",
                "expected_return_date",
                "actual_return_date",
            },
        )
        self.assertEqual(serializer.data["book"]["title"], "Test Book")

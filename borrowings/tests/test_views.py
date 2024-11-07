from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from borrowings.models import Borrowing
from books.models import Book

User = get_user_model()


class BorrowingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="adminpass",
            email="adminuser@example.com",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="Paperback",
            inventory=5,
            daily_fee=10.0,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
        )

        self.client.force_authenticate(user=self.user)

    def test_borrowing_create(self):
        data = {
            "book": self.book.id,
            "user": self.user.id,
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=1),
        }

        response = self.client.post("/borrowings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_borrowing_list_for_specific_user(self):
        response = self.client.get("/borrowings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Only 1 borrowing for the user

    def test_borrowing_list_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/borrowings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # The admin should be able to see the borrowing

    def test_return_book(self):
        url = f"/borrowings/{self.borrowing.id}/return/"
        data = {"actual_return_date": date.today().isoformat()}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(self.borrowing.actual_return_date, date.today())

        self.assertEqual(self.book.inventory, 6)

    def test_borrowing_return_book_already_returned(self):
        self.borrowing.actual_return_date = date.today()
        self.borrowing.save()

        url = f"/borrowings/{self.borrowing.id}/return/"
        data = {"actual_return_date": date.today()}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Book already returned")

    def test_borrowing_filter_by_user_id(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/borrowings/?user_id=" + str(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_borrowing_filter_by_active_status(self):
        self.borrowing.actual_return_date = None
        self.borrowing.save()

        response = self.client.get("/borrowings/?is_active=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

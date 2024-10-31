from django.db import models
from rest_framework.exceptions import ValidationError

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.expected_return_date <= self.borrow_date:
            raise ValidationError(
                "Expected return date must be after borrow date."
            )
        if (
            self.actual_return_date
            and self.actual_return_date < self.borrow_date
        ):
            raise ValidationError(
                "Actual return date cannot be before the borrow date."
            )

    def __str__(self):
        return f"Borrowed on {self.borrow_date}"

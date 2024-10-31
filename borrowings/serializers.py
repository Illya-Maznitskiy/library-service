from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = [
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]

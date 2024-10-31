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

    def validate(self, attrs):
        borrow_date = attrs.get("borrow_date")
        expected_return_date = attrs.get("expected_return_date")
        actual_return_date = attrs.get("actual_return_date")

        if expected_return_date <= borrow_date:
            raise serializers.ValidationError(
                "Expected return date must be after borrow date."
            )

        if actual_return_date and actual_return_date < borrow_date:
            raise serializers.ValidationError(
                "Actual return date cannot be before the borrow date."
            )

        return attrs

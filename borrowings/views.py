from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter borrowings by user ID and active status."""
        queryset = super().get_queryset()
        user = self.request.user
        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date=None)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if not user.is_staff:
            return queryset.filter(user=user)

        return queryset

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        """Return a book and update its return date."""
        borrowing = self.get_object()

        if borrowing.actual_return_date is None:
            actual_return_date = request.data.get("actual_return_date")

            if actual_return_date:
                borrowing.actual_return_date = actual_return_date
                borrowing.book.inventory += 1
                borrowing.save()

                serializer = BorrowingDetailSerializer(borrowing)

                return Response(
                    {
                        "status": "Book returned successfully",
                        "borrowing": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Actual return date is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"error": "Book already returned"},
            status=status.HTTP_400_BAD_REQUEST,
        )

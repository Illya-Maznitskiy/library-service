from rest_framework import viewsets, permissions

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

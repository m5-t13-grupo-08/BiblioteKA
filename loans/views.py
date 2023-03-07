from rest_framework.generics import ListCreateAPIView
from .models import Loan
from .serializers import LoanSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from books.models import Copy, Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound


class LoanView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        found_copy = book.copies.filter(is_free=True).first()

        if not found_copy:
            raise NotFound("Livro indisponível")

        found_copy.is_free = False
        found_copy.save()

        serializer.save(user=self.request.user, copy=found_copy)

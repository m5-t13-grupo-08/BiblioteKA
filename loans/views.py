from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
)
from rest_framework.views import APIView, Request, Response, status
from .models import Loan
from datetime import datetime
from users.models import User
from .serializers import LoanSerializer
from django.shortcuts import get_object_or_404
from books.models import Copy, Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from loans.permissions import LoanPermission
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, date


class LoanView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [LoanPermission]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        user = get_object_or_404(User, pk=self.kwargs.get("user_id"))

        found_copy = (
            book.copies.filter(
                is_free=True,
            )
            .order_by("id")
            .first()
        )

        if not found_copy:
            raise NotFound("Livro indisponível")

        found_copy.is_free = False
        found_copy.save()

        deadline = date.today() + timedelta(days=15)

        if deadline.strftime("%A") == "Saturday":
            deadline = deadline + timedelta(days=2)

        if deadline.strftime("%A") == "Sunday":
            deadline = deadline + timedelta(days=1)

        serializer.save(user=user, copy=found_copy, deadline=deadline)

    def get_queryset(self):
        queryset = self.queryset.filter(user__id=self.kwargs.get("user_id"))
        return queryset


class LoanDetailView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_url_kwarg = "loan_id"

    def perform_destroy(self, instance):
        loan = get_object_or_404(Loan, pk=self.kwargs.get("loan_id"))

        instance.copy.is_free = True
        print(instance)
        instance.devolution_date = datetime.now()


class LoanHistoricView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.views import APIView, Request, Response, status
from .models import Book, Copy
from .serializers import BookSerializer, CopySerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
import ipdb


class BookView(ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = "book_id"


class CopyView(ListCreateAPIView):
    serializer_class = CopySerializer
    queryset = Copy.objects.all()
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        serializer.save(book=book)


class CopyDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CopySerializer
    queryset = Copy.objects.all()
    lookup_url_kwarg = "copy_id"


class FollowBookView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, book_id: str) -> Response:
        book = get_object_or_404(Book, id=book_id)
        book.followed_by.add(request.user)

        return Response(
            {"message": "Book successfully folowed!"}, status.HTTP_202_ACCEPTED
        )

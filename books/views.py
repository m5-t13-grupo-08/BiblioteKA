from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView, Request, Response, status
from .models import Book, Copy
from .serializers import BookSerializer, CopySerializer, FollowSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from books.permissions import BookPermission
from rest_framework.permissions import IsAuthenticated


class BookView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [BookPermission]

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


class FollowBookView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        book.followed_by.add(self.request.user)
        book.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Book successfully followed!"},
            status=status.HTTP_202_ACCEPTED,
            headers=headers,
        )


class UnfollowBookView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "book_id"

    def perform_destroy(self, instance):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        book.followed_by.remove(self.request.user)
        book.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Book successfully unfollowed!"},
            status=status.HTTP_202_ACCEPTED,
        )

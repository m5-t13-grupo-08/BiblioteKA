from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.views import APIView, Request, Response, status
from .models import Book, Copy
from .serializers import BookSerializer, CopySerializer
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


class FollowBookView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"

    def perform_update(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        book.followed_by.add(self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(
            {"message": "Book successfully followed!"}, status.HTTP_202_ACCEPTED
        )

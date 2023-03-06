from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
)
from .models import Book, Copy
from .serializers import BookSerializer, CopySerializer
from django.shortcuts import get_object_or_404


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


class CopyDetailView(RetrieveDestroyAPIView):
    serializer_class = CopySerializer
    queryset = Copy.objects.all()
    lookup_url_kwarg = "copy_id"

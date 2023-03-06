from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Copy
from .serializers import BookSerializer


class BookView(ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_url_kwarg = "book_id"

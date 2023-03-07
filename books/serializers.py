from rest_framework import serializers

from .models import Book, Copy


class BookSerializer(serializers.ModelSerializer):
    copies = serializers.SerializerMethodField()

    def get_copies(self, obj: Copy):
        copies_count = obj.copies.all().count()
        return copies_count

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "page_number",
            "publisher",
            "cdu",
            "copies",
            "followed_by",
        ]
        read_only_fields = ["followed_by"]


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = [
            "id",
            "book",
            "buyed_at",
            "price",
            "sector",
        ]
        read_only_fields = ["book"]

from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    books_title = serializers.SerializerMethodField()

    def get_user_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username

    def get_books_title(self, obj):
        return obj.copy.book.title

    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "username",
            "user_email",
            "books_title",
            "copy",
            "loan_date",
            "deadline",
            "devolutions_date",
            "renovations",
        ]
        read_only_fields = [
            "user",
            "copy",
            "loan_date",
            "deadline",
            "devolutions_date",
        ]

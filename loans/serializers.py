from rest_framework import serializers

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "copies",
            "loan_date",
            "devolutions_date",
            "renovations",
        ]
        read_only_fields = [
            "user",
            "copies",
            "loan_date",
            "devolutions_date",
        ]

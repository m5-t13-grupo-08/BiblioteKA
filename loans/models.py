from django.db import models
import uuid


class Loan(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    copy = models.ForeignKey(
        "books.Copy",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    loan_date = models.DateField(auto_now_add=True)
    devolutions_date = models.DateField(null=True)
    renovations = models.IntegerField(null=True)

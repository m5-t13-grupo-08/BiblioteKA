from django.db import models
import uuid


class Loan(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="loan",
    )
    loan_date = models.DateField()
    devolutions_date = models.DateField()
    renovations = models.IntegerField()

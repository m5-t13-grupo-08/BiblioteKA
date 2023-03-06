from django.db import models
import uuid


class Sector(models.TextChoices):
    general_collection = "general_collection"
    restauration = "restauration"
    lost = "lost"
    technical_treatment = "technical_treatment"


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(null=False, max_length=80)
    author = models.CharField(null=False, max_length=40)
    page_number = models.IntegerField(null=False)
    publisher = models.CharField(max_length=40)
    cdu = models.CharField(null=False, max_length=50)
    followed_by = models.ManyToManyField(
        "users.User",
        related_name="followed_books",
    )


class Copy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    buyed_at = models.DateField()
    price = models.FloatField()
    sector = models.CharField(
        max_length=20,
        choices=Sector.choices,
        default=Sector.general_collection,
        null=False,
    )
    is_free = models.BooleanField(default=True)
    loan = models.ForeignKey(
        "loans.Loan",
        on_delete=models.CASCADE,
        related_name="copies",
        null=True,
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )

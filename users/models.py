from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Situation(models.TextChoices):
    normal = "normal"
    debt = "debt"
    disconnected = "disconnected"
    suspended = "suspended"
    
class UserCategory(models.TextChoices):
    graduation = "graduation" #15 dias
    post_graduation = "post_graduation" #30 dias
    collaborator = "collaborator" #30 dias

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField()
    user_category = models.CharField(
        choices=UserCategory.choices, default=UserCategory.graduation, null=False
    )
    first_name = models.CharField()
    last_name = models.CharField()
    username = models.CharField() #matricula
    password = models.CharField()
    situation = models.CharField(
        max_length=20, choices=Situation.choices, default=Situation.normal, null=False
    )
    address = models.ForeignKey(".Address", on_delete=models.CASCADE, related_name='user')

class Address(models.Model):
    zip_code = models.CharField()
    uf = models.CharField()
    complement = models.TextField()
    telephone = models.CharField()
    street = models.CharField()
    district = models.CharField()
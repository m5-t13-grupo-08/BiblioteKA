from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "zip_code",
            "uf",
            "complement",
            "telephone",
            "street",
            "district",
        ]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    address = AddressSerializer(required=True)

    def create(self, validated_data: dict) -> User:
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "user_category",
            "first_name",
            "last_name",
            "username",
            "password",
            "situation",
            "address",
            "is_superuser",
        ]
        extra_kwargs = {"password": {"write_only": True}}

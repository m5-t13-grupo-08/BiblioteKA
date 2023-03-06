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
    is_superuser = serializers.BooleanField(allow_null=True, default=False)

    def create(self, validated_data: dict) -> User:
        if validated_data["is_superuser"]:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user

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

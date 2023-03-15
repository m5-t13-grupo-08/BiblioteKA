from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Address
from datetime import datetime


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

    situation = serializers.SerializerMethodField()

    def get_situation(self, obj) -> str:
        today = datetime.now()
        is_in_debt = (
            obj.loans.filter(
                deadline__lt=today,
            )
            .filter(devolutions_date=None)
            .first()
        )

        if is_in_debt:
            is_in_debt.user.situation = "debt"
            is_in_debt.user.save()

        return obj.situation

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and (request.method == "POST" or request.method == "PATCH"):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    def create(self, validated_data: dict) -> User:
        if validated_data["is_superuser"]:
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

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
            "followed_books",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "followed_books": {"read_only": True},
        }

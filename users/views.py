from django.shortcuts import render
from rest_framework.views import Request, Response, status
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, AddressSerializer
from .models import User, Address

# Create your views here.


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        address_data = serialized.validated_data.pop("address")
        address_obj = Address.objects.create(**address_data)

        user = User.objects.create(**serialized.validated_data, address=address_obj)
        final_serialization = UserSerializer(user)

        return Response(final_serialization.data, status.HTTP_201_CREATED)

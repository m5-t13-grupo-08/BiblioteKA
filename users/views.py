from rest_framework.views import Response, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import UserSerializer
from .models import User, Address


class UserCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        address_data = serialized.validated_data.pop("address")
        address_obj = Address.objects.create(**address_data)

        serialized.save(address=address_obj)

        return Response(serialized.data, status.HTTP_201_CREATED)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

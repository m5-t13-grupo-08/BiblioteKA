from rest_framework.views import Response, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import UserSerializer
from .models import User, Address
from .permissions import UserPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserCreateView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return User.objects.all()

        return User.objects.filter(
            id=self.request.user.id,
        )

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

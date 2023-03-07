from rest_framework.generics import ListCreateAPIView
from .models import Loan
from .serializers import LoanSerializer
from django.shortcuts import get_object_or_404
from users.models import User
from books.models import Copy
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoanView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_url_kwarg = "copy_id"

    def perform_create(self, serializer):
        copy = get_object_or_404(Copy, pk=self.kwargs.get("copy_id"))
        if not copy.is_free:
            print("não permitir emprestimo")

        copy.is_free = False
        copy.save()

        serializer.save(user=self.request.user, copy=copy)

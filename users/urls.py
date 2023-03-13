from django.urls import path
from . import views
from loans import views as loanViews
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.UserCreateView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("users/<str:user_id>/", views.UserDetailView.as_view()),
    path("user/loan/historic/", loanViews.LoanHistoricView.as_view()),
]

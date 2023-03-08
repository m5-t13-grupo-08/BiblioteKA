from django.urls import path
from . import views
from loans.views import LoanView

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<str:book_id>/", views.BookDetailView.as_view()),
    path("books/<str:book_id>/copy/", views.CopyView.as_view()),
    path("books/copy/<str:copy_id>/", views.CopyDetailView.as_view()),
    path("users/<str:user_id>/books/<str:book_id>/loan/", LoanView.as_view()),
    path("books/<str:book_id>/follow/", views.FollowBookView.as_view()),
    path("user/<str:user_id>/loans/", LoanView.as_view()),
]

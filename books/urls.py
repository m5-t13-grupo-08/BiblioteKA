from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<str:book_id>/", views.BookDetailView.as_view()),
    path("books/<str:book_id>/copy/", views.CopyView.as_view()),
    path("books/copy/<str:copy_id>/", views.CopyDetailView.as_view()),
]
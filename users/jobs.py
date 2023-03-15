from django.core.mail import send_mail
from django.conf import settings
from books.models import Book, Copy


def schedule_api():
    bookList = Book.objects.all()
    for book in bookList:
        copyList = Copy.objects.filter(book_id=book.id)
        users = book.followed_by.all()
        atleast_one_copy_free = False
        for copy in copyList:
            if copy.is_free:
                atleast_one_copy_free = True

        if atleast_one_copy_free:
            users_email = []
            for user in users:
                users_email.append(user.email)
            send_mail(
                subject=f"O livro {book.title} está disponível para leitura!",
                message=f"{book.title} está disponível, venha até a BiblioteKA busca-lo e exercite sua leitura!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=users_email,
                fail_silently=False,
            )

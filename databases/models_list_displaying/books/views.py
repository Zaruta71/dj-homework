from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'

    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, template, context)


def date_view(request, pub_date):
    template = 'books/date_view.html'

    books = Book.objects.filter(pub_date=pub_date)
    previous_book = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    next_book = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    context = {
        'books': books,
        'previous_book': previous_book,
        'next_book': next_book,
    }

    return render(request, template, context)

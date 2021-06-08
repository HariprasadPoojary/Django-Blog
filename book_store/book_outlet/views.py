from django.shortcuts import render

# Create your views here.
from .models import Book


def index(request):
    all_books = Book.objects.all()
    context = {
        "all_books": all_books,
    }
    return render(request, "book_outlet/index.html", context)


def book_detail(request, book_title):
    book_title_s = " ".join(book_title.split("-"))
    print(book_title_s)
    book = Book.objects.get(title__iexact=book_title_s)
    print(book)
    context = {
        "book": book,
    }
    return render(request, "book_outlet/book_detail.html", context)
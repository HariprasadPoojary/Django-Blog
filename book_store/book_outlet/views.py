from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

# Create your views here.
from .models import Book


def index(request):
    all_books = Book.objects.all().order_by("-rating")  # "-" to order in descending
    all_books_count = all_books.count()
    all_ratings_avg = all_books.aggregate(Avg("rating"))
    context = {
        "all_books": all_books,
        "all_books_count": all_books_count,
        "all_ratings_avg": all_ratings_avg,
    }
    return render(request, "book_outlet/index.html", context)


def book_detail(request, book_title):
    try:
        book = Book.objects.get(slug=book_title)
    except ObjectDoesNotExist:
        # There are many objects without slug field
        book_title_s = " ".join(book_title.split("-"))  # Get title
        # get object by searching title
        book = Book.objects.get(title__istartswith=book_title_s[:5])
        # save object to add slug field
        book.save()
        # reload the page so that try block can execute successfully
        return redirect("book_detail", book_title=book_title)
    except:
        raise Http404

    # # * Instead of try-catch use below function
    # book = get_object_or_404(Book, slug=book_title)

    context = {
        "book": book,
    }

    return render(request, "book_outlet/book_detail.html", context)
from django.db import models

# for _ in class book_rating due to error --> NameError: name '_' is not defined
from django.utils.translation import gettext as _

# Create your models here.
class Book(models.Model):
    BOOK_RATING = [
        (None, "(Unknown)"),
        (1, "Poor"),
        (2, "Fair"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    ]
    title = models.CharField(max_length=100)
    pages = models.IntegerField(null=True)
    author = models.CharField(max_length=50, null=True)
    rating = models.IntegerField(choices=BOOK_RATING)
    is_bestselling = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}, rating - {self.rating}"


# Queries practiced usign Django shell

# >>> from book_outlet.models import Book
# >>> django = Book(title="Django Unchained", rating=4)
# >>> django.save()
# >>> mehula = Book(title="Immortals of Mehula", rating=4)
# >>> mehula.save()
# >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>
# >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>

# * Create and Save at the same time
# >>> Book.objects.create(title="50 Shades of Grey", author="E. L. James", rating=5, pages=250)
# <Book: 50 Shades of Grey, rating - 5>
# >>> Book.objects.create(title="50 Shades Darker", author="E. L. James", rating=5, pages=300)
# <Book: 50 Shades Darker, rating - 5>
# >>> Book.objects.create(title="50 Shades Creed", author="E. L. James", rating=5, pages=280)
# <Book: 50 Shades Creed, rating - 5>
# >>> Book.objects.create(title="Da Vinci Code", author="Dan Brown", rating=4, pages=450)
# <Book: Da Vinci Code, rating - 4>
# >>> Book.objects.create(title="Angels & Demons", author="Dan Brown", rating=4, pages=550)
# <Book: Angels & Demons, rating - 4>

# * get must return only 1 object else MultipleObjectsReturned Exception
# Book.objects.get(id=2)
# <Book: Immortals of Mehula, rating - 4>

# * Use of filter to get multiple objects in return
# >>> Book.objects.filter(author="E. L. James")
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>]>
# >>> Book.objects.filter(author="E. L. James", pages=300)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>]>
# >>> Book.objects.filter(author="E. L. James", pages__gt=200)
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>]>
# >>> Book.objects.filter(author="E. L. James", pages__gt=280)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>]>

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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
    slug = models.SlugField(
        default="", null=False, db_index=True
    )  # db_index is used to increase the performance by storing the data more efficiently

    # define a function to return url from model itself
    def get_absolute_url(self):
        if self.slug:
            slug_text = self.slug
            print(f"slug model: {slug_text}")
        else:
            slug_text = slugify(self.title)

        return reverse("book_detail", args=[slug_text])

    # *Override Django's save method to populate slug field
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)

    #     # *IMP call super class' save method to make sure other operations work as expected
    #     super().save(*args, **kwargs)
    # ? Save is not required anymore because of prepopulated_fields in admin.py

    def __str__(self) -> str:
        return f"{self.title}, rating - {self.rating}"


# ! Queries practiced using Django shell

# ? >>> from book_outlet.models import Book
# >>> django = Book(title="Django Unchained", rating=4)
# >>> django.save()
# >>> mehula = Book(title="Immortals of Mehula", rating=4)
# >>> mehula.save()
# * >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>
# * >>> Book.objects.all()
# <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>

# ! Create and Save at the same time
# * >>> Book.objects.create(title="50 Shades of Grey", author="E. L. James", rating=5, pages=250)
# <Book: 50 Shades of Grey, rating - 5>
# * >>> Book.objects.create(title="50 Shades Darker", author="E. L. James", rating=5, pages=300)
# <Book: 50 Shades Darker, rating - 5>
# * >>> Book.objects.create(title="50 Shades Creed", author="E. L. James", rating=5, pages=280)
# <Book: 50 Shades Creed, rating - 5>
# * >>> Book.objects.create(title="Da Vinci Code", author="Dan Brown", rating=4, pages=450)
# <Book: Da Vinci Code, rating - 4>
# * >>> Book.objects.create(title="Angels & Demons", author="Dan Brown", rating=4, pages=550)
# <Book: Angels & Demons, rating - 4>

# ! get must return only 1 object else MultipleObjectsReturned Exception
# Book.objects.get(id=2)
# <Book: Immortals of Mehula, rating - 4>

# ! Use of filter to get multiple objects in return
# * >>> Book.objects.filter(author="E. L. James")
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>]>
# * >>> Book.objects.filter(author="E. L. James", pages=300)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>]>
# * >>> Book.objects.filter(author="E. L. James", pages__gt=200)
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>]>
# * >>> Book.objects.filter(author="E. L. James", pages__gt=280)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>]>

# ! Quering objects with OR condition, by default normal filters act like AND condition
# ? >>> from django.db.models import Q
# * >>> Book.objects.filter(Q(author="E. L. James") | Q(pages__gt=280))
# <QuerySet [<Book: Django Unchained, rating - 4>, <Book: Immortals of Mehula, rating - 4>, <Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>, <Book: Da Vinci Code, rating - 4>, <Book: Angels & Demons, rating - 4>]>
# * >>> Book.objects.filter(Q(author="E. L. James") | Q(author="Dan Brown"))
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>, <Book: Da Vinci Code, rating - 4>, <Book: Angels & Demons, rating - 4>]>

# ! Quering objects with OR & AND condition, by default normal filters act like AND condition
# * >>> Book.objects.filter(Q(author="E. L. James") | Q(author="Dan Brown"), pages__gt=280)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>, <Book: Da Vinci Code, rating - 4>, <Book: Angels & Demons, rating - 4>]>

# ! We can cache the results in Django to increase performance by reducing the database hit
# * >>> james_brown = Book.objects.filter(Q(author="E. L. James") | Q(author="Dan Brown"))
# * >>> james_brown.filter(pages__gt=280)
# <QuerySet [<Book: 50 Shades Darker, rating - 5>, <Book: Da Vinci Code, rating - 4>, <Book: Angels & Demons, rating - 4>]>
# * >>> james_brown.filter(rating__gt=4)
# <QuerySet [<Book: 50 Shades of Grey, rating - 5>, <Book: 50 Shades Darker, rating - 5>, <Book: 50 Shades Creed, rating - 5>]>
# * >>> james_brown_page = james_brown.filter(pages__gt=280)
# * >>> james_brown_page.filter(author="E. L. James")
# <QuerySet [<Book: 50 Shades Darker, rating - 5>]>

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=100)
    pincode = models.IntegerField(validators=[MaxValueValidator(999999)])
    city = models.CharField(max_length=60)

    def __str__(self) -> str:
        return f"{self.street}, {self.city}"

    class Meta:
        verbose_name_plural = "Address Entries"


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


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
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books"
    )
    rating = models.IntegerField(choices=BOOK_RATING)
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(
        default="", null=False, db_index=True
    )  # db_index is used to increase the performance by storing the data more efficiently
    published_country = models.ManyToManyField(Country, related_name="books")

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
# * >>> django = Book(title="Django Unchained", rating=4)
# * >>> django.save()
# * >>> mehula = Book(title="Immortals of Mehula", rating=4)
# * >>> mehula.save()
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
# * >>> Book.objects.get(id=2)
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

# ! Adding data with Foreign Key -> Many-to-One Relationship
# ? >>> from book_outlet.models import Book, Author
# * >>> mp = Author.objects.get(first_name="Mario")
# * >>> mp.last_name
# 'Puzo'
# * >>> tgf = Book(title="The Godfather", rating=5, pages=700, is_bestselling=False, author=mp)
# * >>> tgf.title
# 'The Godfather'
# * >>> tgf.author
# <Author: Mario Puzo>
# * >>> tgf.author.first_name
# 'Mario'

# ! Cross Model Quering (Foreign Key)
# * >>> Book.objects.filter(author__last_name = "James")
# <QuerySet [<Book: Fifty Shades of Grey, rating - 5>, <Book: Fifty Shades Darker, rating - 4>, <Book: Fifty Shades Creed, rating - 5>]>
# * >>> Book.objects.filter(author__last_name__contains = "ames")
# <QuerySet [<Book: Fifty Shades of Grey, rating - 5>, <Book: Fifty Shades Darker, rating - 4>, <Book: Fifty Shades Creed, rating - 5>]>
# ? Reverse Many to one relationship
# * >>> ej = Author.objects.get(last_name="James")
# * >>> ej.book_set
# <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x00000265AE543D00>
# * >>> ej.book_set.all()
# <QuerySet [<Book: Fifty Shades of Grey, rating - 5>, <Book: Fifty Shades Darker, rating - 4>, <Book: Fifty Shades Creed, rating - 5>]>
# ? Add related_name="books" to author(ForeignKey) field in Book Model,
# ? *** ej.book_set.all() wont work anymore ***
# * >>> ej.books.all()
# <QuerySet [<Book: Fifty Shades of Grey, rating - 5>, <Book: Fifty Shades Darker, rating - 4>, <Book: Fifty Shades Creed, rating - 5>]>
# * >>> ej.books.filter(rating__gt = 4)
# <QuerySet [<Book: Fifty Shades of Grey, rating - 5>, <Book: Fifty Shades Creed, rating - 5>]>

# ! One-to-One Relatioship
# * >>> addr = Address.objects.get(city="Mangalore")
# * >>> addr.street
# 'Sampige'
# * >>> ej = Author.objects.get(last_name="James")
# * >>> ej.address
# <Address: Mangalore>
# * >>> addr.author
# <Author: E. L. James>
# * >>> addr.author.first_name
# 'E. L.'
# * >>> addr.author.last_name
# 'James'

# ! Many-to-Many Relatioship
# * >>> ind = Country.objects.get(name="India")
# * >>> ind.code
# 'IN'
# * >>> fg = Book.objects.get(title="Forrest Gump")
# * >>> fg.published_country
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x000002411E815940>
# * >>> fg.published_country = ind
# ? TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use published_country.set() instead.
# * >>> fg.published_country.add(ind)
# * >>> fg.published_country
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x000002411E84AF40>
# * >>> fg.published_country.get(code="IN")
# <Country: India>
# * >>> fg.published_country.get(code="US")
# ? book_outlet.models.Country.DoesNotExist: Country matching query does not exist.
# ? Reverse link
# * >>> ind.books.all()
# ? books being the value -> related_name="books" of published_country in Book model
# ? else query would be ind.book_set.all()
# <QuerySet [<Book: Fifty Shades Creed, rating - 5>, <Book: Forrest Gump, rating - 4>]>
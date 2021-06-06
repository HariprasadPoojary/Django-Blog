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
    title = models.CharField(max_length=50)
    rating = models.IntegerField(choices=BOOK_RATING)

    # ? OR
    # class book_rating(models.IntegerChoices):
    #     # https://docs.djangoproject.com/en/3.1/ref/models/fields/
    #     POOR = 1, _("Poor")
    #     FAIR = 2, _("Fair")
    #     GOOD = 3, _("Good")
    #     VERY_GOOD = 4, _("Very Good")
    #     EXCELLENT = 5, _("Excellent")
    #     # No Rating
    #     __empty__ = _("(Unknown)")

    # rating = models.IntegerField(choices=book_rating.choices)

    def __str__(self) -> str:
        return self.title
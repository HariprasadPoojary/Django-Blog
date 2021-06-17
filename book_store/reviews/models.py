from django.db import models

# Create your models here.
class Review(models.Model):
    username = models.CharField(max_length=100)
    review_text = models.TextField(max_length=500)
    RATINGS = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]
    rating = models.IntegerField(choices=RATINGS)

    def __str__(self) -> str:
        return f"{self.username}, {self.rating}"
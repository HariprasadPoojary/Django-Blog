from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.caption}"

    def get_absolute_url(self):
        return reverse("posts_tags", args=[self.caption])


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=300)
    post_image = models.ImageField(upload_to="post_images", null=True)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(db_index=True, unique=True)
    content = models.TextField(validators=[MinLengthValidator(50)])
    # Relations
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.SET_NULL,
    )
    tag = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("post_details", args=[self.slug])


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    comment_text = models.TextField(max_length=500)
    time = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.user_name}, {self.user_email}"
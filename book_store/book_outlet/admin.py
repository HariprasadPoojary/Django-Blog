from django.contrib import admin

# Register your models here.
from .models import Book, Author


class AuthorAdmin(admin.ModelAdmin):
    ...


class BookAdmin(admin.ModelAdmin):
    # readonly_fields = ("slug",) # not required now, because of below
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "author",
        "rating",
    )
    list_display = ("title", "author", "rating")


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
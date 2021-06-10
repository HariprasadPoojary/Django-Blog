from django.contrib import admin

# Register your models here.
from .models import Book


class BookAdmin(admin.ModelAdmin):
    # readonly_fields = ("slug",) # not required now, because of below
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "author",
        "rating",
    )
    list_display = ("title", "author", "rating")


admin.site.register(Book, BookAdmin)
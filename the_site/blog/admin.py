from django.contrib import admin

# Register your models here.
from .models import Author, Tag, Post, Comment


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": (
            "title",
            "author",
        )
    }
    list_display = (
        "title",
        "author",
    )
    list_filter = (
        "title",
        "author",
        "tag",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "comment_text",
        "time",
    )


admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
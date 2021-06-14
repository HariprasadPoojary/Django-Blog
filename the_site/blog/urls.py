from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts, name="posts"),
    path("posts/<slug:post_slug>/", views.post_details, name="post_details"),
    path("posts/tags/<str:caption>/", views.post_tags, name="posts_tags"),
]

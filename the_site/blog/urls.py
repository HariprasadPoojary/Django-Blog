from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path(
        "posts/<slug:post_slug>/", views.PostDetailsView.as_view(), name="post_details"
    ),
    path("posts/tags/<str:caption>/", views.PostTagsView.as_view(), name="posts_tags"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("posts/", views.posts, name="posts"),
    path("posts/<slug:post_slug>", views.post_details, name="post_details"),
]

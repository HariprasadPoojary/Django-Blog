from django.shortcuts import render
from datetime import date

# Create your views here.
from .models import Post

# dummy post detail content


def index(request):
    recent_posts = Post.objects.order_by("date")[:4]
    context = {
        "recent_posts": recent_posts,
    }
    return render(request, "blog/index.html", context)


def posts(request):
    all_posts = Post.objects.all()
    context = {
        "posts": all_posts,
    }
    return render(request, "blog/all_posts.html", context)


def post_details(request, post_slug):
    the_post = Post.objects.get(slug=post_slug)
    context = {
        "the_post": the_post,
    }

    return render(request, "blog/post-details.html", context)
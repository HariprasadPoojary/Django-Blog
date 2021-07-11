from django.shortcuts import get_object_or_404, render

# Create your views here.
from .models import Post, Tag


def index(request):
    recent_posts = Post.objects.order_by("-date")[:3]  # "-" for descending
    context = {
        "recent_posts": recent_posts,
    }
    return render(request, "blog/index.html", context)


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    context = {
        "posts": all_posts,
    }
    return render(request, "blog/all_posts.html", context)


def post_details(request, post_slug):
    # the_post = Post.objects.get(slug=post_slug)1
    the_post = get_object_or_404(Post, slug=post_slug)
    post_tags = the_post.tag.all()
    context = {
        "the_post": the_post,
        "tags": post_tags,
    }

    return render(request, "blog/post-details.html", context)


def post_tags(request, caption):
    tag = Tag.objects.get(caption=caption)
    all_posts = tag.post_set.all().order_by("-date")

    context = {
        "posts": all_posts,
    }
    return render(request, "blog/all_posts.html", context)
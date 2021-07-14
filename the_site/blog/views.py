from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Post, Tag
from .forms import CommentForm


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


# ! Class Based Views


# class IndexView(TemplateView):
#     template_name = "blog/index.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         recent_posts = Post.objects.order_by("-date")[:3]  # "-" for descending
#         context["recent_posts"] = recent_posts

#         return context


class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "recent_posts"
    ordering = ["-date"]  # "-" for descending

    def get_queryset(self):
        data_set = super().get_queryset()
        data_set = data_set[:3]  # limiting to 3 objects

        return data_set


# class PostsView(TemplateView):
#     template_name = "blog/all_posts.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         all_posts = Post.objects.all("-date")  # "-" for descending
#         context["posts"] = all_posts

#         return context


class PostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]  # "-" for descending


class PostDetailsView(DetailView):
    template_name = "blog/post-details.html"
    model = Post
    # slug_field = "slug"  # Slug field name from Model
    slug_url_kwarg = "post_slug"  # Slug variable name in urls.py
    context_object_name = "the_post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_tags = self.object.tag.all()
        context["tags"] = post_tags
        # load form
        comment_form = CommentForm()

        # add to context
        context["comment_form"] = comment_form

        return context


class PostTagsView(ListView):
    template_name = "blog/all_posts.html"
    model = Tag
    context_object_name = "posts"

    def get_queryset(self, **kwargs):
        tag_data_set = super().get_queryset()
        tag_data_set = tag_data_set.get(caption=self.kwargs["caption"])
        all_posts = tag_data_set.post_set.all().order_by("-date")

        return all_posts

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic import View

# Create your views here.
from .models import Post, Tag
from .forms import CommentForm

# ! Function Based Views

# def index(request):
#     recent_posts = Post.objects.order_by("-date")[:3]  # "-" for descending
#     context = {
#         "recent_posts": recent_posts,
#     }
#     return render(request, "blog/index.html", context)


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     context = {
#         "posts": all_posts,
#     }
#     return render(request, "blog/all_posts.html", context)


# def post_details(request, post_slug):
#     # the_post = Post.objects.get(slug=post_slug)1
#     the_post = get_object_or_404(Post, slug=post_slug)
#     post_tags = the_post.tag.all()
#     context = {
#         "the_post": the_post,
#         "tags": post_tags,
#     }

#     return render(request, "blog/post-details.html", context)


# def post_tags(request, caption):
#     tag = Tag.objects.get(caption=caption)
#     all_posts = tag.post_set.all().order_by("-date")

#     context = {
#         "posts": all_posts,
#     }
#     return render(request, "blog/all_posts.html", context)


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


# class PostDetailsView(DetailView):
#     template_name = "blog/post-details.html"
#     model = Post
#     # slug_field = "slug"  # Slug field name from Model
#     slug_url_kwarg = "post_slug"  # Slug variable name in urls.py
#     context_object_name = "the_post"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post_tags = self.object.tag.all()
#         context["tags"] = post_tags
#         # load form
#         comment_form = CommentForm()

#         # add to context
#         context["comment_form"] = comment_form

#         return context


class PostDetailsView(View):
    """
    return dictionary containing post model object, tags object(with all tags related to the post) and comments related to posts
    """

    def get_post_tags(self, the_slug):
        the_post = Post.objects.get(slug=the_slug)
        post_tags = the_post.tag.all()
        # query comments from post -> One to Many relation
        post_comments = the_post.comment_set.all().order_by("-time")

        return {
            "the_post": the_post,
            "tags": post_tags,
            "comments": post_comments,
        }

    def get(self, request, post_slug):
        # get post & tags
        post_n_tags = self.get_post_tags(post_slug)
        the_post = post_n_tags["the_post"]
        post_tags = post_n_tags["tags"]
        post_comments = post_n_tags["comments"]
        read_later = (
            True if post_slug in request.session.get("read_later_posts") else False
        )
        print(read_later)
        # form
        comment_form = CommentForm()

        context = {
            "the_post": the_post,
            "tags": post_tags,
            "comment_form": comment_form,
            "comments": post_comments,
            "read_later": read_later,
        }

        return render(request, "blog/post_details.html", context)

    def post(self, request, post_slug):
        # get post
        post_n_tags = self.get_post_tags(post_slug)
        the_post = post_n_tags["the_post"]

        # form
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Don't save the form to database yet
            comment = comment_form.save(commit=False)
            # assign post object to comment model object
            comment.post = the_post
            # save the object to database
            comment.save()

            return redirect("post_details", post_slug=post_slug)
        else:
            # get tags
            post_tags = post_n_tags["tags"]
            # get comments
            post_comments = post_n_tags["comments"]

            context = {
                "the_post": the_post,
                "tags": post_tags,
                "comment_form": comment_form,
                "comments": post_comments,
            }

            return render(request, "blog/post-details.html", context)


class PostTagsView(ListView):
    template_name = "blog/all_posts.html"
    model = Tag
    context_object_name = "posts"

    def get_queryset(self, **kwargs):
        tag_data_set = super().get_queryset()
        tag_data_set = tag_data_set.get(caption=self.kwargs["caption"])
        all_posts = tag_data_set.post_set.all().order_by("-date")

        return all_posts


class StoreReadLaterView(View):
    def post(self, request):
        post_later_slug = request.POST["post_slug"]
        if request.session.get("read_later_posts") is not None:
            # key read_later_posts is available, append post
            post_later_slug_list = request.session["read_later_posts"]
            post_later_slug_list.append(post_later_slug)
            request.session["read_later_posts"] = post_later_slug_list
        else:
            # key read_later_posts is not yet available, create a list with value
            request.session["read_later_posts"] = [post_later_slug]

        return redirect("post_details", post_slug=post_later_slug)


class DoneReadLaterView(View):
    def post(self, request):
        post_later_slug = request.POST["post_slug"]
        post_later_slug_list = request.session["read_later_posts"]
        post_later_slug_list.remove(post_later_slug)
        request.session["read_later_posts"] = post_later_slug_list

        return redirect("post_details", post_slug=post_later_slug)


class ReadLaterView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self, **kwargs):
        posts_data_set = super().get_queryset()
        posts_list = self.request.session.get("read_later_posts", [])
        posts_data_set = self.model.objects.filter(slug__in=posts_list)

        return posts_data_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["read_later"] = True
        return context

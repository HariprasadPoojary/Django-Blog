from django.shortcuts import render

# Create your views here.
from datetime import date

# dummy post detail content
all_posts = [
    {
        "slug": "the-mountains",
        "image": "mountains.jpg",
        "author": "Hariprasad",
        "date": date(2021, 6, 5),
        "title": "Why I Adore Mountains",
        "excerpt": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.",
        "content": """
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        """,
    },
    {
        "slug": "the-coding",
        "image": "coding.jpg",
        "author": "Hariprasad",
        "date": date(2021, 6, 5),
        "title": "Why I Love Python",
        "excerpt": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.",
        "content": """
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.

        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore dicta illum repudiandae officia fuga repellat.
        """,
    },
]


def index(request):
    sorted_post = sorted(all_posts, key=lambda post: post["date"])
    recent_posts = sorted_post[-2:]
    context = {
        "posts": recent_posts,
    }
    return render(request, "blog/index.html", context)


def posts(request):
    context = {
        "posts": all_posts,
    }
    return render(request, "blog/all_posts.html", context)


def post_details(request, post_slug):
    context = {
        "the_post": None,
    }
    for post in all_posts:
        if post["slug"] == post_slug:
            context["the_post"] = post
            break

    return render(request, "blog/post-details.html", context)
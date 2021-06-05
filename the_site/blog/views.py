from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, "blog/index.html", context)


def posts(request):
    context = {}
    return render(request, "blog/all_posts.html", context)


def post_details(request, post_slug):
    context = {}
    return render(request, "blog/post-details.html", context)
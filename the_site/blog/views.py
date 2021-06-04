from django.shortcuts import render

# Create your views here.
def landing_page(request):
    context = {}
    return render(request, "blog/index.html", context)


def posts(request):
    context = {}
    return render(request, "blog/posts.html", context)


def post_details(request, post_slug):
    ...
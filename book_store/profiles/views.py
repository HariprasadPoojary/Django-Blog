from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from . import file_ops


class CreateProfileView(View):
    def get(self, request):
        return render(request, "profiles/create_profile.html")

    def post(self, request):
        print(request.FILES["image"])
        file_ops.save_file(request.FILES["image"])
        return redirect("create_profile")
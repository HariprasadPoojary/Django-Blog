from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView

# Create your views here.
from . import file_ops
from .forms import CreateProfileForm
from .models import UserProfile


class UserProfileCreateView(CreateView):
    model = UserProfile
    template_name = "profiles/create_profile.html"
    fields = "__all__"
    success_url = "/profile/"


# * with normal view class
# class CreateProfileView(View):
#     def get(self, request):
#         form = CreateProfileForm()
#         context = {"form": form}
#         return render(request, "profiles/create_profile.html", context)

#     def post(self, request):
#         submitted_form = CreateProfileForm(request.POST, request.FILES)
#         if submitted_form.is_valid():
#             user_image = UserProfile(user_image=request.FILES["user_image"])
#             user_image.save()
#             # file_ops.save_file(request.FILES["image"])
#             return redirect("create_profile")
#         else:
#             context = {"form": submitted_form}
#             return render(request, "profiles/create_profile.html", context)


class ProfileView(ListView):
    model = UserProfile
    template_name = "profiles/user_profiles.html"
    context_object_name = "profiles"
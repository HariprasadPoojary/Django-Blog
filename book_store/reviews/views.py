import reviews
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

# Create your views here.
from .forms import ReviewForm
from .models import Review


# def review(request):

#     # * Basic Form code
#     # if request.method == "POST":
#     #     user_name = request.POST["username"]
#     #     context = {"username": user_name}
#     #     # return render(request, "reviews/thankyou.html", context)
#     #     return redirect("thank_you")
#     # return render(request, "reviews/review.html", context)

#     # * Django Form
#     if request.method == "POST":
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             # * For the form with only Form class
#             # print(form.cleaned_data)
#             # rev = Review()
#             # rev.username = form.cleaned_data["username"]
#             # rev.review_text = form.cleaned_data["review_text"]
#             # rev.rating = form.cleaned_data["rating"]
#             # rev.save()

#             # * Form with ModelForm
#             form.save()

#             return redirect("thank_you")
#     else:
#         form = ReviewForm()

#     context = {
#         "form": form,
#     }

#     return render(request, "reviews/review.html", context)


# def thank_you(request):
#     context = {}
#     return render(request, "reviews/thankyou.html", context)


# * Class Based views


# * class ReviewView(View):
#     def get(self, request):
#         form = ReviewForm()

#         context = {
#             "form": form,
#         }
#         return render(request, "reviews/review.html", context)

#     def post(self, request):
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("thank_you")
#         else:
#             context = {
#                 "form": form,
#             }
#         return render(request, "reviews/review.html", context)


# * class ReviewView(FormView):
#     template_name = "reviews/review.html"
#     form_class = ReviewForm
#     success_url = "/review/thank-you"

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class ReviewView(CreateView):
    # model = Review # * in case there is no pre-defined ModelForm class available
    template_name = "reviews/review.html"
    # * form class needs to be ModelForm to save data automatically
    form_class = ReviewForm
    success_url = "/review/thank-you"


class ThankYouView(TemplateView):
    template_name = "reviews/thankyou.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = "Hari"
        return context


# * class ReviewsView(TemplateView):
#     template_name = "reviews/reviews.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         reviews = Review.objects.all()
#         context["reviews"] = reviews
#         return context


class ReviewsView(ListView):
    template_name = "reviews/reviews.html"
    model = Review
    context_object_name = "reviews"

    # * Apply condition on queryset/data for rendering
    # def get_queryset(self):
    #     data_set = super().get_queryset()
    #     data_set = data_set.filter(rating__gt=4)
    #     return data_set


# * class ReviewDetailView(TemplateView):
#     template_name = "reviews/review_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         self.the_review = Review.objects.get(id=kwargs["pk"])
#         print(self.the_review.username)
#         context["the_review"] = self.the_review
#         return context


class ReviewDetailView(DetailView):
    template_name = "reviews/review_detail.html"
    model = Review
    context_object_name = "the_review"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the object of model review
        loaded_review = self.object
        # get the request object
        request = self.request
        # check if session review id = loaded review id & store bool
        context["is_favorite"] = str(loaded_review.id) == request.session.get(
            "favorite_review"
        )
        # print(str(loaded_review.id), request.session["favorite_review"])
        # print(context["is_favorite"])
        return context


class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        review_id = review_id.strip()
        request.session["favorite_review"] = review_id

        return redirect("review_detail", pk=review_id)
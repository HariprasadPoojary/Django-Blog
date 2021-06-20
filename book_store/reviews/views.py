import reviews
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView

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


class ReviewView(View):
    def get(self, request):
        form = ReviewForm()

        context = {
            "form": form,
        }
        return render(request, "reviews/review.html", context)

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thank_you")
        else:
            context = {
                "form": form,
            }
        return render(request, "reviews/review.html", context)


class ThankYouView(TemplateView):
    template_name = "reviews/thankyou.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = "Hari"
        return context


class ReviewsView(TemplateView):
    template_name = "reviews/reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        context["reviews"] = reviews
        return context


class ReviewDetailView(TemplateView):
    template_name = "reviews/review_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.the_review = Review.objects.get(id=kwargs["id"])
        print(self.the_review.username)
        context["the_review"] = self.the_review
        return context

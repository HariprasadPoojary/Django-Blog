from django.shortcuts import redirect, render

# Create your views here.
from .forms import ReviewForm


def review(request):

    # * Basic Form code
    # if request.method == "POST":
    #     user_name = request.POST["username"]
    #     context = {"username": user_name}
    #     # return render(request, "reviews/thankyou.html", context)
    #     return redirect("thank_you")
    # return render(request, "reviews/review.html", context)

    # * Django Form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect("thank_you")
    else:
        form = ReviewForm()

    context = {
        "form": form,
    }

    return render(request, "reviews/review.html", context)


def thank_you(request):
    context = {}
    return render(request, "reviews/thankyou.html", context)

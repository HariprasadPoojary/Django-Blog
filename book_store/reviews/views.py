from django.shortcuts import redirect, render

# Create your views here.
def review(request):

    if request.method == "POST":
        user_name = request.POST["username"]
        context = {"username": user_name}
        # return render(request, "reviews/thankyou.html", context)
        return redirect("thank_you")

    context = {}
    return render(request, "reviews/review.html", context)


def thank_you(request):
    context = {}
    return render(request, "reviews/thankyou.html", context)

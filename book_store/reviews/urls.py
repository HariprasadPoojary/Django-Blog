from django.urls import path
from . import views

urlpatterns = [
    # path("", views.review, name="review"),
    # path("thank-you/", views.thank_you, name="thank_you"),
    path("", views.ReviewView.as_view(), name="review"),
    path("reviews/", views.ReviewsView.as_view(), name="reviews"),
    path("reviews/favorite/", views.AddFavoriteView.as_view(), name="reviews_favorite"),
    path("thank-you/", views.ThankYouView.as_view(), name="thank_you"),
    path(
        "review-detail/<str:pk>/",
        views.ReviewDetailView.as_view(),
        name="review_detail",
    ),
]
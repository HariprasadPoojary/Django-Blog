from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserProfileCreateView.as_view(), name="create_profile"),
]

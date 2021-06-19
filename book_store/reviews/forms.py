from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        # exclude = ["owner_comment"]

        labels = {
            "username": "Your Name",
            "review_text": "Your Review",
        }
        error_messages = {
            "username": {
                "required": "Your Name must not be empty",
                "max_length": "Please enter a shorter name",
            },
            "review_text": {
                "required": "Please enter some review",
                "max_length": "Please enter a shorter review",
            },
        }


# class ReviewForm(forms.Form):
#     username = forms.CharField(
#         label="Your Name",
#         max_length=100,
#         error_messages={
#             "required": "Your Name must not be empty",
#             "max_length": "Please enter a shorter name",
#         },
#     )
#     review_text = forms.CharField(
#         label="Your Review",
#         widget=forms.Textarea,
#         max_length=500,
#         error_messages={
#             "required": "Your Name must not be empty",
#             "max_length": "Please enter a shorter name",
#         },
#     )
#     RATINGS = [
#         (1, "⭐"),
#         (2, "⭐⭐"),
#         (3, "⭐⭐⭐"),
#         (4, "⭐⭐⭐⭐"),
#         (5, "⭐⭐⭐⭐⭐"),
#     ]
#     rating = forms.ChoiceField(
#         label="Rating",
#         widget=forms.Select,
#         choices=RATINGS,
#     )

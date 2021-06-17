from django import forms


class ReviewForm(forms.Form):
    username = forms.CharField(
        label="Your Name",
        max_length=100,
        error_messages={
            "required": "Your Name must not be empty",
            "max_length": "Please enter a shorter name",
        },
    )
    review_text = forms.CharField(
        label="Your Review",
        widget=forms.Textarea,
        max_length=500,
        error_messages={
            "required": "Your Name must not be empty",
            "max_length": "Please enter a shorter name",
        },
    )
    RATINGS = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]
    rating = forms.ChoiceField(
        label="Rating",
        widget=forms.Select,
        choices=RATINGS,
    )
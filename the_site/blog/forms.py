from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["post"]

        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "comment_text": "Comment",
        }

        error_messages = {
            "user_name": {
                "required": "Please enter user name!",
                "max_length": "Please enter a shorter name",
            },
            "user_email": {
                "required": "Please enter email id!",
            },
            "comment_text": {
                "required": "Please enter some comment!",
                "max_length": "Please enter a shorter name",
            },
        }
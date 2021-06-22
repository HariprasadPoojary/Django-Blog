from django import forms


class CreateProfileForm(forms.Form):
    user_image = forms.ImageField(allow_empty_file=False, label="Select Image")

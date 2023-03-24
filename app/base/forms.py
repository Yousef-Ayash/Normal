from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        min_length=4,
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"Placeholder": "Tell us the title of your story."}
        ),
    )

    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["slug"]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"
        exclude = ["post"]

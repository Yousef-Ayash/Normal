from django import forms

from .models import Comment, Post


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
        exclude = ["slug", "owner"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

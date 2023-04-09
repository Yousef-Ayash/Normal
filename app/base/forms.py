from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, User


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
        exclude = ["slug", "owner", "likes"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "password1", "password2", "avatar", "bio"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()
        if commit:
            user.save()
        return user

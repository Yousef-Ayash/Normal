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
        exclude = ["slug", "owner", "likes", "is_published"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "avatar", "bio"]

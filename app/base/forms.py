from django import forms
from django.contrib.auth import password_validation

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


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_confirm = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ["name", "username", "password", "password_confirm", "avatar", "bio"]

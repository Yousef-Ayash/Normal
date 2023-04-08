# from accounts.forms import UserForm
# from accounts.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import CommentForm, PostForm, UserForm
from .models import Comment, Post, User


class LoginView(TemplateView):
    def get(self, request):
        page = "login"
        if request.user.is_authenticated:
            return redirect("home")

        context = {"page": page}
        return render(request, "base/login_register.html", context)

    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid Username or Password")
            return redirect("login")

        user_name = user.username
        pass_word = user.password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, f"User: {user} - Username: {user_name} - Password: {pass_word}"
            )
            return redirect("login")


def logoutUser(request):
    logout(request)
    return redirect("home")


class RegisterView(TemplateView):
    def get(self, request):
        form = UserForm()

        context = {"form": form}
        return render(request, "base/login_register.html", context)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, form.errors.as_text())
            return redirect("register")


class HomeView(TemplateView):
    def get(self, request):
        posts = Post.objects.filter(is_published=True).all()
        context = {"posts": posts}
        return render(request, "base/home.html", context)


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class CreatePostView(TemplateView):
    def get(self, request):
        form = PostForm()

        context = {"form": form}
        return render(request, "base/post_form.html", context)

    def post(self, request):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            return redirect("home")


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class UpdatePostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        form = PostForm(instance=post)

        if request.user != post.owner:
            return HttpResponse("YOU Are Not Allowed HERE!")

        context = {"form": form}
        return render(request, "base/post_form.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        form = PostForm(request.POST or None, request.FILES, instance=post)

        if form.is_valid():
            form.save()

            return redirect("home")


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class DeletePostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)

        if request.user != post.owner:
            return HttpResponse("YOU Are Not Allowed HERE!")

        return render(request, "base/delete.html", {"post": post})

    def post(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        post.delete()
        return redirect("home")


@method_decorator(login_required(login_url="login"), name="post")
class PostView(TemplateView):
    def get(self, request, username=None, slug=None):
        user = User.objects.get(username=username)
        post = Post.objects.get(owner=user, slug=slug)
        comment_form = CommentForm()
        comments = Comment.objects.filter(post=post).all()

        context = {"post": post, "form": comment_form, "comments": comments}
        return render(request, "base/post_view.html", context)

    def post(self, request, username=None, slug=None):
        user = User.objects.get(username=username)
        post = Post.objects.get(owner=user, slug=slug)
        comment_form = CommentForm(request.POST or None)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.owner = request.user
            comment.post = post
            comment.save()
            return redirect("post", username=username, slug=slug)


@login_required(login_url="login")
def post_like_toggle(request, username=None, slug=None):
    user_ = User.objects.get(username=username)
    post = Post.objects.get(owner=user_, slug=slug)
    user = request.user
    if user.is_authenticated:
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

    return redirect("post", username=username, slug=slug)

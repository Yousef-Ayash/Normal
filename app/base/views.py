from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from .forms import CommentForm, PostForm, CustomUserRegistrationForm
from .models import Comment, Post, User


class RegisterView(FormView):
    form_class = CustomUserRegistrationForm
    template_name = 'base/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user
        return redirect('home')  # Redirect to the desired page after successful registration and login


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

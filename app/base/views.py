from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from .forms import CommentForm, CustomUserRegistrationForm, PostForm, UserForm
from .models import Comment, Post, Topic, User


class RegisterView(FormView):
    form_class = CustomUserRegistrationForm
    template_name = "base/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class HomeView(TemplateView):
    def get(self, request):
        q = request.GET.get("q") if request.GET.get("q") != None else ""

        posts = Post.objects.filter(
            Q(owner__name__icontains=q)
            | Q(owner__username__icontains=q)
            | Q(topic__name__exact=q)
            | Q(title__icontains=q)
        ).filter(is_published=True)

        topics = Topic.objects.all()

        context = {"posts": posts, "topics": topics}
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

            if "draft" in request.POST:
                post.is_published = False
            elif "publish" in request.POST:
                post.is_published = True

            post.owner = request.user
            post.save()

            return redirect("post", request.user.username, post.slug)


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class UpdatePostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        form = PostForm(instance=post)

        if request.user != post.owner:
            raise PermissionDenied

        context = {"form": form}
        return render(request, "base/post_form.html", context)

    def post(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        form = PostForm(request.POST or None, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)

            if "draft" in request.POST:
                post.is_published = False
            elif "publish" in request.POST:
                post.is_published = True

            post.save()

            return redirect("post", request.user.username, post.slug)


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class DeletePostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)

        if request.user != post.owner:
            raise PermissionDenied

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

        if request.user != post.owner and post.is_published == False:
            raise PermissionDenied

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


class UserView(TemplateView):
    def get(self, request, username=None):
        user = User.objects.get(username=username)

        posts = Post.objects.filter(owner__username=username).all()
        posts_others = (
            Post.objects.filter(owner__username=username)
            .filter(is_published=True)
            .all()
        )

        context = {"user": user, "posts": posts, "posts_others": posts_others}
        return render(request, "base/user_view.html", context)


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class UserUpdate(TemplateView):
    def get(self, request):
        user = request.user
        form = UserForm(instance=user)

        context = {"form": form}
        return render(request, "base/update_profile.html", context)

    def post(self, request):
        user = request.user
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect("user-profile", request.user.username)


@method_decorator(login_required(login_url="login"), name="get")
@method_decorator(login_required(login_url="login"), name="post")
class DeleteProfile(TemplateView):
    def get(self, request):
        user = request.user

        return render(request, "base/delete_profile.html", {"user": user})

    def post(self, request):
        user = request.user
        dl_c = request.POST.get("dl-confirm")

        if dl_c == f"Delete {request.user.username}":
            user.delete()
            return redirect("home")
        else:
            return redirect("delete-account")


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

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import PostForm
from .models import Post


class HomeView(TemplateView):
    def get(self, request):
        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, "base/home.html", context)


class CreatePostView(TemplateView):
    def get(self, request):
        page = "create"
        form = PostForm()

        context = {"form": form, "page": page}
        return render(request, "base/post_form.html", context)

    def post(self, request):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect("home")


class UpdatePostView(TemplateView):
    def get(self, request, slug=None):
        page = "update"
        post = Post.objects.get(slug=slug)
        form = PostForm(instance=post)

        context = {"form": form, "page": page}
        return render(request, "base/post_form.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        form = PostForm(request.POST or None, request.FILES, instance=post)

        if form.is_valid():
            form.save()

            return redirect("home")


class DeletePostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        return render(request, "base/delete.html", {"post": post})

    def post(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        post.delete()
        return redirect("home")


class PostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)

        context = {"post": post}
        return render(request, "base/post_view.html", context)

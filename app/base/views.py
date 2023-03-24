from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import Post, Image
from .forms import PostForm

# from .forms import


class HomeView(TemplateView):
    def get(self, request):
        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, "base/home.html", context)


class CreatePostView(TemplateView):
    def get(self, request):
        form = PostForm()
        images = Image.objects.all()

        context = {"form": form, "images": images}
        return render(request, "base/post_form.html", context)

    def post(self, request):
        form = PostForm(request.POST or None, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            image = request.FILES.get("image")
            caption = request.POST.get("img-caption")

            post.save()
            Image.objects.create(post=post, image=image, caption=caption)

            return redirect("home")


class PostView(TemplateView):
    def get(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        images = Image.objects.filter(post__slug=slug)

        context = {"post": post, "images": images}
        return render(request, "base/post_view.html", context)


# images = request.FILES.getlist('images')
#         for image in images:
#             MultipleImage.objects.create(images=image)

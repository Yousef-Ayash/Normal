from django.contrib import admin
from .models import Post, Image


class PostCreate(admin.ModelAdmin):
    list_display = ["title", "slug", "cover_img"]
    search_fields = ["title", "slug", "cover_img"]
    list_per_page = 10


class ImageCreate(admin.ModelAdmin):
    list_display = ["post", "image", "caption"]
    search_fields = ["post", "image", "caption"]
    list_per_page = 10


admin.site.register(Post, PostCreate)
admin.site.register(Image, ImageCreate)

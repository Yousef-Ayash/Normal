from django.contrib import admin

from .models import Post


class PostCreate(admin.ModelAdmin):
    list_display = ["owner", "title", "slug"]
    search_fields = ["owner", "title", "slug"]
    list_per_page = 10


admin.site.register(Post, PostCreate)

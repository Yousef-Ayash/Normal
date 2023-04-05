from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "slug"]
    search_fields = ["title", "owner", "slug"]
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "owner", "content"]
    search_fields = ["post", "owner", "content"]
    list_per_page = 10


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

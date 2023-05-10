from django.contrib import admin

from .models import Comment, Post, Topic, User


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "slug"]
    search_fields = ["title", "owner", "slug"]
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "owner", "content"]
    search_fields = ["post", "owner", "content"]
    list_per_page = 10


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "username", "date_joined"]
    search_fields = ["name", "username", "date_joined"]
    list_per_page = 10


class TopicAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    list_per_page = 10


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)

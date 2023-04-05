from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField

# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name="Post Title")
    slug = models.SlugField(null=True, blank=True, unique=True)
    content = QuillField()

    # likes = models.ManyToManyField(User, related_name="post_likes")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}/"

    def get_total_likes(self):
        return self.likes.users.count()

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.content[:16]}"


# class Like(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
#     post = models.OneToOneField(Post, on_delete=models.CASCADE, null=False)

#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.owner.username} liked "{self.post.title[:30]}"'

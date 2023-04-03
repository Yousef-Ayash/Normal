from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField

# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name="Post Title")
    slug = models.SlugField(null=True, blank=True, unique=True)
    # content = models.TextField(verbose_name="Post Content", null=False, blank=False)
    content = QuillField()
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

    class Meta:
        ordering = ["-created_at"]

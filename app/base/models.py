from django.db import models
from django.utils.text import slugify

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Post Title")
    slug = models.SlugField(null=True, blank=True, unique=True)
    content = models.TextField(verbose_name="Post Content", null=False, blank=False)
    cover_img = models.ImageField(verbose_name="Cover Image")
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


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Post Image", blank=True)
    caption = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f"{self.image.name} of {self.post.title[:10]}"

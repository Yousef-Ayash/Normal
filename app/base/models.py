from cryptography.fernet import Fernet
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django_quill.fields import QuillField

key = Fernet.generate_key()
fernet = Fernet(key)

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="default_avatar.png")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Topic(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, verbose_name="Post Title")
    slug = models.SlugField(null=True, blank=True, unique=False)
    content = QuillField()
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(null=False, default=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        enc_title = fernet.encrypt(self.title.encode())
        enc_title_ = str(enc_title)

        if self.slug is None:
            self.slug = f"{slugify(self.title)}_{enc_title_[10:26:2]}"

        super().save(*args, **kwargs)

    def get_like_url(self):
        return reverse(
            "post:like-toggle",
            kwargs={"slug": self.slug},
        )

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.content[:16]}"


@receiver(pre_save, sender=User)
def pre_save_image(sender, instance, *args, **kwargs):
    """Function to delete the avatar pic from the server after updating it"""
    try:
        old_img_name = instance.__class__.objects.get(id=instance.id).avatar
        if str(old_img_name) == "default_avatar.png":
            return

        old_img = instance.__class__.objects.get(id=instance.id).avatar.path

        try:
            new_img = instance.avatar.path
        except:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

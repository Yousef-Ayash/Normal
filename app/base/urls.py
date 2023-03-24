from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("create-post", views.CreatePostView.as_view(), name="create-post"),
    path("post/<slug:slug>", views.PostView.as_view(), name="post"),
]

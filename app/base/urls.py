from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("create", views.CreatePostView.as_view(), name="create-post"),
    path("update/<slug:slug>", views.UpdatePostView.as_view(), name="update-post"),
    path("delete/<slug:slug>", views.DeletePostView.as_view(), name="delete-post"),
    path("post/<slug:slug>", views.PostView.as_view(), name="post"),
]

from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("", views.HomeView.as_view(), name="home"),
    path(
        "create-post",
        views.CreatePostView.as_view(),
        name="create-post",
    ),
    path(
        "update-post/<slug:slug>",
        views.UpdatePostView.as_view(),
        name="update-post",
    ),
    path(
        "delete/<slug:slug>",
        views.DeletePostView.as_view(),
        name="delete-post",
    ),
    path("post/<slug:slug>", views.PostView.as_view(), name="post"),
]
